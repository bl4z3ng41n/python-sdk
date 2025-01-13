from anon_python_sdk import ControlClient

client = ControlClient()

try:
    client.connect()
    circuits = client.get_circuits()
    for circuit in circuits:
        print(f"Circuit ID: {circuit.id}, Status: {circuit.status}")
        print(f"  Purpose: {circuit.purpose}")
        print(f"  Time Created: {circuit.time_created}")
        print("  Path:")
        for relay in circuit.path:
            print(f"    Fingerprint: {relay.fingerprint}, Nickname: {relay.nickname}")
finally:
    client.close()