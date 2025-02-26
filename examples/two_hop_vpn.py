from anon_python_sdk import Control, Process, Config, Socks, StreamStatus

print("Starting Anon...")
# Create a configuration
config = Config(
    auto_terms_agreement=True,
    display_log=False
)

# Initialize and start the runner
anon = Process.launch_anon(anonrc_path=config.to_file())

control = Control.from_port()
socks = Socks()

try:
    print("Connecting to Control Port...")
    control.authenticate()

    relays = control.get_relays()
    print("Total Relays:", len(relays))
    nl_relays = control.filter_relays_by_countries(relays, "de")
    exit_relays = control.filter_relays_by_flags(nl_relays, "Exit")
    exit = exit_relays[0].fingerprint
    print("Exit Relay:", exit)
    guard_relays = control.filter_relays_by_flags(nl_relays, "Guard")
    guard = guard_relays[0].fingerprint
    print("Guard Relay:", guard)

    print("Creating a new circuit through specified relays")
    path = [guard, exit]
    circuit_id = control.new_circuit(path=path, await_build=True)
    print(f"New circuit created with ID: {circuit_id}")

    circuit = control.get_circuit(circuit_id)
    print(f"Created circuit. ID: {circuit.id}, Path: {circuit.path}")

    control.disable_stream_attachment()
    print("Stream attachment disabled.")

    def attach_stream(stream):
        print(f"Stream status: {stream.status}. Purpose: {stream.purpose}")
        if stream.status == StreamStatus.NEW.name:
            control.attach_stream(stream.id, circuit_id)

    control.add_event_listener(attach_stream)
    print("Stream listener added.")

    print("Executing a new get request...")

    resp = socks.get("http://ip-api.com/json")
    print(resp.text)

    control.remove_event_listener(attach_stream)
    print("Stream listener removed.")

    print("Closing the manual circuit...")
    control.close_circuit(circuit_id)
    print(f"Manual circuit {circuit_id} closed successfully.")

finally:
    control.close()
    print("Controller connection closed.")

    print("Stopping Anon...")
    anon.stop()
