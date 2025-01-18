from anon_python_sdk.control_client import ControlClient
from anon_python_sdk import start_anon, stop_anon
import time

print("Starting Anon...")
pid = start_anon()
print(f"Anon started with PID: {pid}")

time.sleep(5)  # Wait for Anon to start

client = ControlClient()

try:
    print("Connecting to Control Port...")
    client.connect()

    print("Creating a new circuit through specified relays...")
    relays = [
        "894D4088C63D3FA4446E505E672C47A8247AC891", 
        "6DB2B0D574CE216648CA388D309EE7CF5DF0B423", 
        "A17C391AAE45689358EC226C43D1290EBED7437A"
        ]# Replace with real relay fingerprints
    m_circuit_id = client.create_circuit(relays)
    print(f"New circuit created with ID: {m_circuit_id}")

    time.sleep(30)  # Wait for the circuit to be established
    m_circuit = client.get_circuit(m_circuit_id)
    print(f"Manual Circuit ID: {m_circuit.id}, Status: {m_circuit.status}, Path: {m_circuit.path}")
    time.sleep(5)

    print("Closing the manual circuit...")
    client.close_circuit(m_circuit_id)
    print(f"Manual circuit {m_circuit_id} closed successfully.")

    r_circuit_id = client.create_circuit()
    print(f"Random circuit created with ID: {r_circuit_id}")

    r_circuit = client.get_circuit(r_circuit_id)
    print(f"Random Circuit ID: {r_circuit.id}, Status: {r_circuit.status}, Path: {r_circuit.path}")

    print("Closing the random circuit...")
    client.close_circuit(r_circuit_id)
    print(f"Random circuit {r_circuit_id} closed successfully.")

finally:
    client.close()
    print("ControlClient connection closed.")

    print("Stopping Anon...")
    stop_anon(pid)
