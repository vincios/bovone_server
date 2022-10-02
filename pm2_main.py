"""
This script helps to run the uvicorn sever with PM2 (https://pm2.keymetrics.io/).
"""
import contextlib
import os
import sys
import threading
import time

import uvicorn
from app.dependencies import get_settings

PM2_IPC_RCV_FD = 3  # PM2 sends IPC messages on FD 3
PM2_IPC_SEND_FD = 4  # PM2 waits for IPC messages on FD 4

config = get_settings()


# We extend the uvicorn Server to add the ability to run (and shutdown) it in a separate thread.
# See https://github.com/encode/uvicorn/issues/742#issuecomment-674411676
class ThreadableServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager  # Define a contex where the server is running
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


if __name__ == "__main__":
    config = uvicorn.Config("app.main:app", host=config.server_host, port=config.server_port, log_level="info")
    server = ThreadableServer(config=config)

    # We run the server on a separate thread to keep the "main" thread free to listen/send PM2 IPC messages
    with server.run_in_thread():
        # Until we are into this context the Server continue to run
        print("Server thread started")
        # PM2 can be configured to waits for a "ready" IPC message to assure that the application is running
        os.write(PM2_IPC_SEND_FD, str.encode("ready"))

        # We run an infinite loop to keep the server running
        while True:
            try:
                # PM2 sends a "shutdown" message when the application should be closed
                ipc_message = os.read(PM2_IPC_RCV_FD, 100)
                ipc_message_str = ipc_message.decode("utf-8")
                print("IPC MESSAGE RECEIVED: ", ipc_message_str)

                if "shutdown" in ipc_message_str.strip().lower():
                    # When PM2 sends a shutdown message we shut down the server.
                    # To gracefully shut down the server, we have only to stop the infinite loop
                    # and let the code exits from the context
                    break

                time.sleep(1)
            except KeyboardInterrupt:
                # We intercept also Ctrl-C events to be sure
                # to gracefully shut down the server also in this situation
                break

    print("Server thread ended")
    sys.exit(0)
