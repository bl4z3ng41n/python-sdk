from anyone_protocol_sdk import Config, Process


# Create a configuration
config = Config(
    auto_terms_agreement=True,
    display_log=True,
)

anon = None

try:
    anon = Process.launch_anon(anonrc_path=config.to_file())
    print("Anon is running...")
except Exception as e:
    print(f"Anon failed to start: {e}")
finally:
    anon.stop()
    print("Anon has stopped.")
