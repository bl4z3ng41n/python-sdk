from anyone_protocol_sdk import Config, Process, Control


# Create a configuration
config = Config(
    auto_terms_agreement=True,
    display_log=True,
)

anon = Process.launch_anon(anonrc_path=config.to_file())

control = Control.from_port()

try:

    control.authenticate()

    fp = "0063916D68A2C7AAC81D98379CCFE21D83E2B5BF"

    microdesc = control.get_microdescriptor(fp)

    print(f"Microdescriptor for {fp}:")
    print(f"Onion Key: {microdesc.onion_key}")
    print(f"NTor Onion Key: {microdesc.ntor_onion_key}")
    print(f"OR Addresses: {microdesc.or_addresses}")
    print(f"Exit Policy: {microdesc.exit_policy}")
    print(f"Exit Policy V6: {microdesc.exit_policy_v6}")
    print(f"Identifiers: {microdesc.identifiers}")
    print(f"Protocols: {microdesc.protocols}")
    print(f"Family: {microdesc.family}")
    print(f"Digest: {microdesc.digest}")
    print()

    print("Anon is running...")
except Exception as e:
    print(f"Anon failed to start: {e}")
finally:
    anon.stop()
    print("Anon has stopped.")
