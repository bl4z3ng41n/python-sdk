from anon_python_sdk import Process, Control, Socks
import time


# Create a configuration as a dictionary
config = {
    "AgreeToTerms": "1",
    "OrPort": "9001",
    "SocksPort": "9050",
    "ControlPort": "9051",
    "Nickname": "anon",
}

anon = None

try:
    def handler(msg):
        print(msg)

    anon = Process.launch_anon_with_config(
        config=config, init_msg_handler=handler)

    print("Anon is running...")

    time.sleep(10)
except Exception as e:
    print(f"Anon failed to start: {e}")
finally:
    anon.stop()
    print("Anon has stopped.")
