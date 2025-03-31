from anyone_protocol_sdk import Control, Process, Config


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
    # circuits = control.get_circuits()

    # # Get relay info from the first relay in the first circuit
    # relay_fingerprint = circuits[0].path[0].fingerprint
    relay_fingerprint = "0E21FF42C6DC8C193B023B20951C2A827F43E84E"
    relay_info = control.get_network_status(relay_fingerprint)
    country = control.get_country(relay_info.address)

    # Fancy print for relay info
    print(f"\n[Relay Info]\n")
    print(f"Nickname: {relay_info.nickname}")
    print(f"Fingerprint: {relay_info.fingerprint}")
    print(f"Address: {relay_info.address}")
    print(f"Country: {country}")
    print(f"OR Port: {relay_info.or_port}")
    print(f"Flags: {', '.join(f.name for f in relay_info.flags)}")
    print(f"Bandwidth: {relay_info.bandwidth} kilobytes/sec")
    print(f"Dir Port: {relay_info.dir_port}")
    print(f"Document: {relay_info.document}")
    print(f"Version line: {relay_info.version_line}")
    print(f"Published: {relay_info.published}")
    print(f"Measured: {relay_info.measured} kilobytes/sec")
    print(f"Is unmeasured: {relay_info.is_unmeasured}")
    print(f"Digest: {relay_info.digest}")
    print(f"Identifier: {relay_info.identifier}")
    print(f"Identifier Type: {relay_info.identifier_type}")
    print(f"OR Addresses: {relay_info.or_addresses}")
    print(f"Version: {relay_info.version}")
    print(f"Unrecognized Entries: {relay_info.unrecognized_bandwidth_entries}")
    print(f"Exit Policy: {relay_info.exit_policy}")
    print(f"Protocols: {relay_info.protocols}")
    print(f"Microdescriptor Hashes: {relay_info.microdescriptor_hashes}")
    print("\n")

finally:
    control.close()
    anon.stop()
