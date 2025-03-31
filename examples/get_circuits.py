from anyone_protocol_sdk import Control, Config, Process


# Create a configuration
config = Config(
    auto_terms_agreement=True
)

# Initialize and start
anon = Process.launch_anon(anonrc_path=config.to_file())
client = Control.from_port()

try:
    client.authenticate()
    circuits = client.get_circuits_with_relay_info_and_country()
    for circuit in circuits:
        print(f"Circuit ID: {circuit['id']}")
        print(f"  Time Created: {circuit['created']}")
        print(f"  Status: {circuit['status']}")
        print(f"  Purpose: {circuit['purpose']}")
        print("  Path:")
        for relay in circuit['relays']:
            print(f"    Fingerprint: {relay['fingerprint']}")
            print(f"    Nickname: {relay['nickname']}")
            print(f"    Address: {relay['address']}")
            print(f"    Country: {relay['country']}")
            print(f"    ORPort: {relay['or_port']}")
            print(f"    Flags: {', '.join(f.name for f in relay['flags'])}")
            print(f"    Bandwidth: {relay['bandwidth']}")
            print()

finally:
    client.close()
    anon.stop()
