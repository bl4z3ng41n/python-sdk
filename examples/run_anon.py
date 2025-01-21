from anon_python_sdk import AnonRunner, AnonConfig
import time

# Create a configuration
config = AnonConfig(
    auto_terms_agreement=True
)

# Initialize and start the runner
runner = AnonRunner(config)

try:
    runner.start()
    print("Anon is running...")
    time.sleep(5)  # Wait for Anon to start
    # Perform tasks
finally:
    runner.stop()
    print("Anon has stopped.")
    exit(0)
