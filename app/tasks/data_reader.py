import asyncio
import csv
import queue
import threading
import time

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from .. import schemas
from ..database import SessionLocal
from ..database.records import save_record
from ..dependencies import get_settings
from ..internal.logger import get_logger
from ..websocket import WebSocketManager

logger = get_logger(__name__)
config = get_settings()


async def start_task(session: Session, ws_manager: WebSocketManager):
    # while True:
    with open(config.data_csv_file_path) as csv_file:
        lines = csv.reader(csv_file, delimiter=";")
        while True:
            try:
                line = next(lines)
                print(line)
                record: schemas.RecordSchema = schemas.RecordSchema.from_csv_line(line)
                save_record(session, record)
                await ws_manager.broadcast(jsonable_encoder(record.dict()))
                await asyncio.sleep(2)
            except csv.Error:
                pass  # skip lines with errors
            except StopIteration:
                break

        # await asyncio.sleep(5)


async def start_task_lite(queue: asyncio.Queue):
    session = SessionLocal()

    with open(config.data_csv_file_path) as csv_file:
        lines = csv.reader(csv_file, delimiter=";")
        while True:
            try:
                line = next(lines)
                print(line)
                record: schemas.RecordSchema = schemas.RecordSchema.from_csv_line(line)
                save_record(session, record)
                # await ws_manager.broadcast(jsonable_encoder(record.dict()))
                await queue.put(record)
                await asyncio.sleep(2)
            except csv.Error:
                pass  # skip lines with errors
            except StopIteration:
                break

    session.close()


class DataReaderThread(threading.Thread):
    def __init__(self, csv_file: str):
        super().__init__()
        self.file_path: str = csv_file
        self._lock: threading.Lock = threading.Lock()
        self._subscribers: set[queue.Queue] = set()
        self._session = SessionLocal()
        self._stop_evt = threading.Event()

    def run(self):
        with open(self.file_path) as csv_file:
            lines = csv.reader(csv_file, delimiter=";")
            while not self._stop_evt.is_set():
                try:
                    line = next(lines)
                    logger.debug("Reading line: %s", line)
                    record: schemas.RecordSchema = schemas.RecordSchema.from_csv_line(line)
                    save_record(self._session, record)
                    # await ws_manager.broadcast(jsonable_encoder(record.dict()))
                    with self._lock:
                        for q in self._subscribers:
                            q.put(record)
                    time.sleep(2)
                except csv.Error:
                    pass  # skip lines with errors
                except StopIteration:
                    break

        self._session.close()

    def subscribe(self) -> queue.Queue:
        q = queue.Queue()
        with self._lock:
            self._subscribers.add(q)

        return q

    def unsubscribe(self, q: queue.Queue):
        with self._lock:
            self._subscribers.remove(q)

    def stop(self):
        self._stop_evt.set()
