from anon_python_sdk import start_anon, stop_anon, create_default_anonrc

# Create a default anonrc file if it doesn't exist
create_default_anonrc()

# Start the Anon process
pid = start_anon()
print(f"Anon started with PID: {pid}")

# Stop the Anon process
stop_anon(pid)
print(f"Anon process with PID {pid} stopped.")
