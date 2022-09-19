from .manager import WebSocketManager

global_manager = WebSocketManager()


def get_manager():
    yield global_manager
