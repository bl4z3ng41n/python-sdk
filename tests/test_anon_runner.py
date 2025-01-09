from anon_python_sdk import start_anon, stop_anon, create_default_anonrc

def test_start_anon():
    print("Creating default anonrc...")
    create_default_anonrc()

    print("Starting Anon...")
    pid = start_anon()
    print(f"Anon started with PID: {pid}")

    print("Stopping Anon...")
    stop_anon(pid)
    print(f"Anon process with PID {pid} stopped successfully!")
