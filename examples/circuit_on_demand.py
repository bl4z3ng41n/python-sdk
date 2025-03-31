import threading
from anyone_protocol_sdk import *
from anon_starter import Anon
import signal
import sys
import stem
import time

config = VPNConfig(
    routings=[
        VPNRouting("ip-api.com", ["de"]),
        VPNRouting("ipinfo.io", ["nl"]),
    ]
)


class AnonRunner:
    def __init__(self):
        self.anon_instance = Anon()
        self.shutdown_event = threading.Event()

        # Register signal handler for graceful exit
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)    

    def run(self):
        print("Starting Anon SDK process...")

        self.anon_instance.control.authenticate()
        print("Authenticated")
        self.anon_instance.control.disable_stream_attachment()
        print("Stream attachment disabled")
        self.anon_instance.control.disable_predicted_circuits()
        print("Predicted circuits disabled")

        streams = {}

        def strem(stream: Stream):
            print(f"Stream: {stream}")
            if not stream.circ_id:
                print(f"Add to wait stream id: {stream.id}")
                if stream.id not in streams:
                    streams[stream.id] = False
                # time.sleep(0.2)

        self.anon_instance.control.add_event_listener(strem, EventType.STREAM)

        # Run shutdown wait in a separate thread
        wait_thread = threading.Thread(
            target=self.wait_for_shutdown, daemon=True)
        wait_thread.start()

        wait_thread_2 = threading.Thread(
            target=self.request, daemon=True)
        wait_thread_2.start()

        time.sleep(5)

        # Keep the main thread active (handling events)
        try:
            while not self.shutdown_event.is_set():
                for stream_id in streams:
                    if streams[stream_id]:
                        continue
                    print(f"got to attach stream id: {stream_id}")
                    circ_id = self.anon_instance.control.new_circuit(await_build=True)
                    print(f"New circuit created with ID: {circ_id}")
                    self.anon_instance.control.attach_stream(stream_id, circ_id)
                    streams[stream_id] = True
                    time.sleep(0.1)
                time.sleep(0.1)

            self.handle_events_forever()
        except KeyboardInterrupt:
            self.handle_exit()

    def wait_for_shutdown(self):
        """Waits for shutdown signal in a separate thread (doesn't block main loop)."""
        self.shutdown_event.wait()
        self.stop()

    def request(self):
        print("Starting socks")
        resp = self.anon_instance.socks.get("http://ip-api.com/json")
        print(resp.text)    

    def handle_events_forever(self):
        """Keeps the SDK running without blocking event handling."""
        while not self.shutdown_event.is_set():
            pass  # Main thread keeps running and handling SDK events

    def handle_exit(self, *args):
        """Handles graceful shutdown on Ctrl+C or SIGTERM."""
        print("\nGracefully shutting down Anon SDK...")
        self.stop()
        sys.exit(0)  # Exit cleanly

    def stop(self):
        if not self.shutdown_event.is_set():
            self.shutdown_event.set()

            try:
                self.anon_instance.stop_vpn()
                print("Anon SDK stopped successfully.")
            except stem.SocketClosed:
                print("Tor control connection already closed. Ignoring error.")
            except Exception as e:
                print(f"Unexpected error during shutdown: {e}")


if __name__ == "__main__":
    runner = AnonRunner()
    runner.run()


# http://ip-api.com/json
# https://ipinfo.io/json
