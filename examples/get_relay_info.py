from anon_python_sdk import Control, Process, Config


# Create a configuration
config = Config(
    auto_terms_agreement=True,
    socks_port=0,
    display_log=False
)

# Initialize and start the runner
anon = Process.launch_anon(anonrc_path=config.to_file())
control = Control.from_port()

try:
    control.authenticate()
    circuits = control.get_circuits()

    # Get relay info from the first relay in the first circuit
    relay_fingerprint = circuits[0].path[0].fingerprint
    relay_info = control.get_network_status(relay_fingerprint)
    country = control.get_country(relay_info.address)

    # Fancy print for relay info
    print(f"\n[Relay Info]\n")
    print(f"Nickname: {relay_info.nickname}")
    print(f"Fingerprint: {relay_info.fingerprint}")
    print(f"Address: {relay_info.address}")
    print(f"Country: {country}")
    print(f"OR Port: {relay_info.or_port}")
    print(f"Flags: {', '.join(relay_info.flags)}")
    print(f"Bandwidth: {relay_info.bandwidth} bytes/sec")


finally:
    control.close()
    anon.stop()
