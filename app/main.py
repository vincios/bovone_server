import asyncio
import logging
from queue import Empty

import uvicorn
from fastapi import FastAPI, WebSocket, Depends
from fastapi.encoders import jsonable_encoder

from . import database
from .dependencies import get_settings
from .internal.logger import get_logger
from .routers import records
from .tasks.data_reader import DataReaderThread
from .websocket import WebSocketManager, get_manager

config = get_settings()

app = FastAPI()
app.include_router(records.router, prefix="/api")

data_reader_task = DataReaderThread(config.data_csv_file_path)
logger = get_logger(__name__)


@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=database.engine)
    # asyncio.create_task(data_reader.start_task_lite(queue))
    logger.info("Starting DataReaderThread")
    data_reader_task.start()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Stopping DataReaderThread")
    data_reader_task.stop()
    data_reader_task.join()
    return


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str, websockets: WebSocketManager = Depends(get_manager)):
    await websockets.broadcast(f"Hello {name}")
    return {"message": f"Hello {name}"}


# @app.get("/startup", status_code=201)
# async def long_endpoint(background_tasks: BackgroundTasks, wsmanager: WebSocketManager = Depends(get_manager),
#                         session: Session = Depends(get_session)):
#     background_tasks.add_task(data_reader.start_task, session, wsmanager)
#     return {"message": "Accepted"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, manager: WebSocketManager = Depends(get_manager)):
    async def on_message(message: str):
        await manager.broadcast(message, websocket)

    logger.info("New websocket connection")
    client = await manager.connect(websocket)
    task = asyncio.create_task(manager.listen(client))

    # queue = client.register_consumer()
    # while True:
    #     data = await queue.get()
    #     await manager.broadcast(data, client)

    queue = data_reader_task.subscribe()
    while not task.done():

        # None of the coroutines called in this block (e.g. send_json())
        # will yield back control to other coroutines. asyncio.sleep() does, and so it will allow
        # the event loop to switch context and serve multiple requests concurrently.
        await asyncio.sleep(0)
        try:
            record = queue.get(block=False)
            # we have to check again because await queue.get is performed int the previous iteration
            # (when task is not already done and the while condition in already True)
            # if not task.done():  # task is done when clients disconnect (see manager.listen())
            await client.websocket.send_json(jsonable_encoder(record.dict()))
        except Empty:
            # if q.get() throws Empty exception, then nothing was available (yet!).
            pass

    data_reader_task.unsubscribe(queue)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.server_port)
