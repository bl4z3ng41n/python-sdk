from anon_python_sdk import *


# Create a configuration
config = Config(
    auto_terms_agreement=True,
    display_log=True,
)

anon = Process.launch_anon(anonrc_path=config.to_file())

control = Control.from_port()
socks = Socks()

try:
    control.authenticate()

    pathRelays = build_circuit_path(control, ["GE", "GR", "FI", "DK"], 2)

    path = [pathRelays[0].fingerprint, pathRelays[1].fingerprint]
    print(path)

    circuit_id = control.new_circuit(path=path, await_build=True)
    circuit = control.get_circuit(circuit_id)
    print(circuit)

    def attach_stream(stream: Stream):
        print(f"Stream status: {stream.status}. Purpose: {stream.purpose}")
        if stream.status == StreamStatus.NEW:
            control.attach_stream(stream.id, circuit_id)

    control.disable_stream_attachment()
    control.add_event_listener(attach_stream, EventType.STREAM)

    resp = socks.get("http://ip-api.com/json")
    print(resp.text)

    control.remove_event_listener(attach_stream)
    control.enable_stream_attachment()
    control.close_circuit(circuit_id)

except Exception as e:
    print(f"Anon failed to start: {e}")
finally:
    control.close()
    anon.stop()
    print("Anon has stopped.")
