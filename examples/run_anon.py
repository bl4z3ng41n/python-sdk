from anon_python_sdk import AnonRunner, AnonConfig


# Create a configuration
config = AnonConfig(
    auto_terms_agreement=True,
    display_log=True,
)

# Initialize and start the runner
runner = AnonRunner(config)

try:
    runner.start(wait_for_ready=False)
    print("Anon is running...")
finally:
    runner.stop()
    print("Anon has stopped.")
    exit(0)
