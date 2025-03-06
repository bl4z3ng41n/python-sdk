from anon_python_sdk import Config, Process, Control, Socks, EventType, AddrMap
import time


# Create a configuration
config = Config(
    auto_terms_agreement=True,
    display_log=True,
)

anon = Process.launch_anon(anonrc_path=config.to_file())
print("Anon is running...")

control = Control.from_port()
socks = Socks()


def print_addr(event: AddrMap):
    print(f"Address: {event.hostname}")
    print(f"IP: {event.destination}")
    print(f"Expires: {event.expiry}")
    print(f"Error: {event.error}")
    print(f"UTC Expiry: {event.utc_expiry}")
    print(f"Cached: {event.cached}")
    print()


try:
    control.authenticate()

    control.add_event_listener(print_addr, EventType.ADDRMAP)

    control.resolve("google.com")
    control.resolve("web3yurii.com")

    time.sleep(3)

except Exception as e:
    print(f"Anon failed to start: {e}")
finally:
    control.remove_event_listener(print_addr)
    anon.stop()
    print("Anon has stopped.")
