from anon_python_sdk import Control, Config, Process


# Create a configuration
config = Config(
    auto_terms_agreement=True
)

# Initialize and start
anon = Process.launch_anon(anonrc_path=config.to_file())
client = Control.from_port()

try:
    client.authenticate()
    circuits = client.get_circuits()
    for circuit in circuits:
        print(f"Circuit ID: {circuit.id}")
        print(f"  Time Created: {circuit.created}")
        print("  Path:")
        for relay in circuit.path:
            print(
                f"    Fingerprint: {relay.fingerprint}, Nickname: {relay.nickname}")
finally:
    client.close()
    anon.stop()
