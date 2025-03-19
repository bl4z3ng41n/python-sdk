from anon_python_sdk import *
import time


# Create a configuration
config = Config(
    auto_terms_agreement=True,
    display_log=True,
)

anon = Process.launch_anon(anonrc_path=config.to_file(), take_ownership=True)

control = Control.from_port()
socks = Socks()

try:
    control.authenticate()

    control.disable_stream_attachment()
    control.disable_predicted_circuits()
    time.sleep(5)

    def attach_stream(stream: Stream):
        print(f"Stream: {stream}")
        if stream.status == StreamStatus.NEW or stream.status == StreamStatus.REMAP or stream.circ_id is None:
            try:
                circuit_id = find_or_create_circuit(control, stream)
                print(f"Attaching stream {stream.id} to circuit {circuit_id}")
                if circuit_id:
                    control.attach_stream(stream.id, circuit_id)
            except Exception as e:
                print(f"Error: {e}")

    control.add_event_listener(attach_stream, EventType.STREAM)

    def warn_log(event: Event):
        if event.type == EventType.WARN:
            print(f"Warn: {event}")

    def info_log(event: Event):
        if event.type == EventType.INFO:
            print(f"Info: {event}")        

    print("Adding warn log listener")
    control.add_event_listener(warn_log, EventType.WARN)
    print("Adding info log listener")
    control.add_event_listener(info_log, EventType.INFO)

    print("Starting socks")
    resp = socks.get("http://ip-api.com/json")
    print(resp.text)

except Exception as e:
    print(f"Anon failed to start: {e}")
finally:
    control.close()
    anon.stop()
    print("Anon has stopped.")
