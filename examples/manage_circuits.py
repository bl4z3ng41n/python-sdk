from anyone_protocol_sdk import Control, Process, Config

print("Starting Anon...")
# Create a configuration
config = Config(
    auto_terms_agreement=True,
    display_log=False
)

# Initialize and start the runner
anon = Process.launch_anon(anonrc_path=config.to_file())

client = Control.from_port()

try:
    print("Connecting to Control Port...")
    client.authenticate()

    print("Creating a new circuit through specified relays...")
    # relays = [
    #     "894D4088C63D3FA4446E505E672C47A8247AC891",
    #     "6DB2B0D574CE216648CA388D309EE7CF5DF0B423",
    #     "A17C391AAE45689358EC226C43D1290EBED7437A"
    #     ]# Replace with real relay fingerprints
    m_circuit_id = client.new_circuit(await_build=True)
    print(f"New circuit created with ID: {m_circuit_id}")

    m_circuit = client.get_circuit(m_circuit_id)
    print(f"Manual Circuit ID: {m_circuit.id}, Path: {m_circuit.path}")

    print("Closing the manual circuit...")
    client.close_circuit(m_circuit_id)
    print(f"Manual circuit {m_circuit_id} closed successfully.")

finally:
    client.close()
    print("Controller connection closed.")

    print("Stopping Anon...")
    anon.stop()
