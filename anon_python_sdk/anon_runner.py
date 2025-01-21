from pathlib import Path
import platform
import subprocess
import threading
from .anon_config import AnonConfig, create_anon_config_file

# Path to the binary directory and default anonrc file
BINARY_DIR = Path.home() / ".anon_python_sdk" / "bin"
DEFAULT_ANONRC = Path("./anonrc")

# Platform-specific binary names
PLATFORM_MAP = {
    "linux": "anon",
    "darwin": "anon",
    "windows": "anon.exe",
}


class AnonRunner:
    """
    Manages the lifecycle of the Anon binary.
    """

    def __init__(self, config: AnonConfig = None):
        """
        Initialize the runner with the given configuration.
        If no configuration is provided, a default configuration is used.
        """
        self.config = self.config = config or AnonConfig()
        self.config_path = None
        self.process = None
        self.log_thread = None

    def log_stream(self):
        """
        Stream logs from the process in a separate thread.
        """
        assert self.process is not None, "Process must be running to stream logs"
        for line in self.process.stdout:
            print(line.decode().strip())    

    def get_binary_path(self) -> Path:
        """
        Determine the path to the Anon binary based on the platform.
        """
        system = platform.system().lower()
        binary_name = PLATFORM_MAP.get(system)

        if not binary_name:
            raise OSError(f"Unsupported platform: {system}")

        binary_path = self.config.binary_path or (BINARY_DIR / binary_name)
        if not binary_path.exists():
            raise FileNotFoundError(f"Anon binary not found at: {binary_path}")
        
        return binary_path

    def start(self):
        """
        Start the Anon binary using the provided configuration.
        """
        # Generate configuration file
        self.config_path = create_anon_config_file(self.config)

        # Command to run Anon
        binary_path = self.get_binary_path()
        command = [str(binary_path), "-f", str(self.config_path)]

        # Start the process
        try:
            if self.config.display_log:
                # Redirect stdout and stderr to the console
                self.process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                print(f"Anon started with PID: {self.process.pid}")

                self.log_thread = threading.Thread(target=self.log_stream, daemon=True)
                self.log_thread.start()
            else:
                # Suppress logs
                self.process = subprocess.Popen(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                print(f"Anon started with PID: {self.process.pid}")

        except FileNotFoundError:
            print(f"Error: Anon binary not found at {binary_path}")
            raise
        except Exception as e:
            print(f"Failed to start Anon: {e}")
            raise

    def stop(self):
        if self.process and self.process.poll() is None:
            print(f"Stopping Anon process with PID: {self.process.pid}")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
                print(f"Anon process with PID {self.process.pid} terminated gracefully.")
            except subprocess.TimeoutExpired:
                print(f"Anon process with PID {self.process.pid} did not stop. Killing it...")
                self.process.kill()
                self.process.wait()
                print(f"Anon process with PID {self.process.pid} killed.")
        else:
            print("Anon process is not running.")

