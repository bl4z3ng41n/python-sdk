from anon_python_sdk import ControlClient, AnonRunner, AnonConfig
import time

print("Starting Anon...")
# Create a configuration
config = AnonConfig(
    auto_terms_agreement=True
)

# Initialize and start the runner
runner = AnonRunner(config)
runner.start()

time.sleep(5)  # Wait for Anon to start

client = ControlClient()

try:
    print("Connecting to Control Port...")
    client.connect()

    print("Creating a new circuit through specified relays...")
    # relays = [
    #     "894D4088C63D3FA4446E505E672C47A8247AC891", 
    #     "6DB2B0D574CE216648CA388D309EE7CF5DF0B423", 
    #     "A17C391AAE45689358EC226C43D1290EBED7437A"
    #     ]# Replace with real relay fingerprints
    m_circuit_id = client.create_circuit()
    print(f"New circuit created with ID: {m_circuit_id}")

    time.sleep(5)  # Wait for the circuit to be established
    m_circuit = client.get_circuit(m_circuit_id)
    print(f"Manual Circuit ID: {m_circuit.id}, Status: {m_circuit.status}, Path: {m_circuit.path}")

    print("Closing the manual circuit...")
    client.close_circuit(m_circuit_id)
    print(f"Manual circuit {m_circuit_id} closed successfully.")

finally:
    client.close()
    print("ControlClient connection closed.")

    print("Stopping Anon...")
    runner.stop()
