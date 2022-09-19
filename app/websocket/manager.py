import asyncio
from functools import partial
from typing import Set, Callable, Optional

from fastapi import WebSocket, WebSocketDisconnect

from ..internal.logger import get_logger

logger = get_logger(__name__)


class WebSocketClient:
    """
        A WebSocketClient handles messages to send to and messages coming from a websocket.
    """
    def __init__(self, websocket: WebSocket):
        self.websocket: WebSocket = websocket
        self.outgoing_messages_queue: asyncio.Queue = asyncio.Queue()
        self.incoming_messages_queues: list[asyncio.Queue] = []

    async def handle_outgoing_messages(self):
        # We use a queue to store messages to send on the websocket, as messages could come from anywhere from the app
        # and this handle is executed (by asyncio) in a separate thread
        while True:
            data = await self.outgoing_messages_queue.get()
            logger.debug("QUEUE: %s (%s)", data, type(data))
            if isinstance(data, dict):
                await self.websocket.send_json(data)
            else:
                await self.websocket.send_text(data)

    async def handle_incoming_messages(self):
        # We use queues to store messages coming from the websocket, as messages could be sent anywhere into the app
        # and this handle is executed (by asyncio) in a separate thread
        # we use multiple outgoing queues, one for each interested consumer
        while True:
            data = await self.websocket.receive_text()
            logger.debug("INCOMING: %s", data)
            for queue in self.incoming_messages_queues:
                await queue.put(data)

    async def send_message(self, message):
        await self.outgoing_messages_queue.put(message)

    def register_consumer(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        self.incoming_messages_queues.append(queue)
        return queue

    def close(self):
        self.outgoing_messages_queue.task_done()
        for queue in self.incoming_messages_queues:
            queue.task_done()


# https://stackoverflow.com/questions/72564515/fastapi-permanently-running-background-task-that-listens-to-postgres-notificati
class WebSocketManager:
    def __init__(self):
        self.connections: Set[WebSocketClient] = set()

    async def connect(self, websocket: WebSocket, on_message=None) -> WebSocketClient:
        """
        This is a blocking method: it loops until the client disconnects.
        So, before it starts to loop, use the callback to communicate the created client
        :param on_message:
        :param websocket:
        :return:
        """
        await websocket.accept()

        ws_client = WebSocketClient(websocket)
        self.connections.add(ws_client)
        return ws_client

    async def listen(self, ws_client: WebSocketClient):
        tasks = [ws_client.handle_outgoing_messages(), ws_client.handle_incoming_messages()]

        # if on_message:
        #     tasks.append(self.listen_client(ws_client, on_message))

        try:
            await asyncio.gather(*tasks)
        except WebSocketDisconnect:
            self.disconnect(ws_client)
            await self.broadcast("Disconnected")

    # async def listen_client(self, client: WebSocketClient, callback):
    #     queue = client.register_consumer()
    #     while True:
    #         data = await queue.get()
    #         if callback and asyncio.iscoroutinefunction(callback):
    #             await callback(data)
    #         elif callback:
    #             callback(data)

    def disconnect(self, client: WebSocketClient):
        # client.close()
        self.connections.remove(client)

    def get_client(self, websocket: WebSocket) -> WebSocketClient:
        # TODO: add a strategy (as a websocket id) to find a websocket into self.connections
        for connection in self.connections:
            if connection.websocket == websocket:
                return connection

    async def send_direct_message(self, websocket: WebSocket, message: str):
        """
        Send a direct message to the websocket
        """
        # TODO: add a strategy (as a websocket id) to find a websocket into self.connections
        await websocket.send_text(message)

    async def broadcast(self, message: str, exclude: WebSocketClient | WebSocket | None = None):
        """
        broadcast a message to all connected clients
        :param exclude:
        :param message:
        :return:
        """
        logger.debug("BROADCAST: %s", message)
        for connection in self.connections:
            if connection != exclude and connection.websocket != exclude:
                await connection.send_message(message)

    async def close_all(self):
        logger.info("Closing all active websockets")
        for connection in self.connections:
            await connection.websocket.close()
