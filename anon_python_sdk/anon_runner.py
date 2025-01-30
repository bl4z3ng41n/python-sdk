from pathlib import Path
import platform
import subprocess
import threading
import re
from typing import Optional
from colorama import Fore, Style, init
from .anon_config import AnonConfig, create_anon_config_file
from .exceptions import AnonError

# Initialize colorama for colored console output
init(autoreset=True)

# Path to the binary directory and default anonrc file
BINARY_DIR = Path.home() / ".anon_python_sdk" / "bin"

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
        self.bootstrap_complete = threading.Event()

    def _get_binary_path(self) -> Path:
        """
        Determine the path to the Anon binary based on the platform.
        """
        system = platform.system().lower()
        binary_name = PLATFORM_MAP.get(system)

        if not binary_name:
            raise OSError(f"{Fore.RED}Unsupported platform: {system}")

        binary_path = self.config.binary_path or (BINARY_DIR / binary_name)
        if not binary_path.exists():
            raise FileNotFoundError(f"{Fore.RED}Anon binary not found at: {binary_path}")
        
        return binary_path

    def start(self, wait_for_ready: bool = True):
        """
        Start the Anon binary using the provided configuration.
        """
        # Generate configuration file
        self.config_path = create_anon_config_file(self.config)

        # Command to run Anon
        binary_path = self._get_binary_path()
        command = [str(binary_path), "-f", str(self.config_path)]

        # Start the process
        try:
            # Capture all output, but only print what’s needed
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            print(f"{Fore.YELLOW}Starting Anon...")

            # Start log monitoring in a separate thread
            self.log_thread = threading.Thread(target=self._monitor_logs, daemon=True)
            self.log_thread.start()
            
            if wait_for_ready:
                # Wait for Anon to reach 100% bootstrap
                self.bootstrap_complete.wait(timeout=60)

                if not self.bootstrap_complete.is_set():
                    raise AnonError(f"{Fore.RED}Anon failed to bootstrap within 60 seconds")
                
                print(f"{Fore.GREEN}Anon is fully bootstrapped and running! PID: {self.process.pid}")

        except FileNotFoundError:
            print(f"{Fore.RED}Error: Anon binary not found at {binary_path}")
            raise
        except Exception as e:
            print(f"{Fore.RED}Failed to start Anon: {e}")
            raise

    def stop(self):
        """
        Stop the Anon process.
        """
        if self.process and self.process.poll() is None:
            print(f"{Fore.YELLOW}Stopping Anon process with PID: {self.process.pid}")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
                print(f"{Fore.GREEN}Anon process terminated gracefully")
            except subprocess.TimeoutExpired:
                print(f"{Fore.RED}Anon process did not stop. Killing it...")
                self.process.kill()
                self.process.wait()
                print(f"{Fore.RED}Anon process killed")
        else:
            print(f"{Fore.RED}Anon process is not running")

    def _monitor_logs(self):
        """
        Monitor Anon logs for bootstrap progress and display logs based on display_log config.
        """
        if self.process is None or self.process.stdout is None:
            return

        for line in iter(self.process.stdout.readline, ''):
            line = line.strip()
            if not line:
                continue

            # Extract bootstrap percentage and message
            bootstrap_match = re.search(r"Bootstrapped (\d+)% \(([^)]+)\): (.+)", line)
            error_match = re.search(r"\[err\]", line, re.IGNORECASE)
            version_match = re.search(r"Anon (\d+\.\d+\.\d+[\w.-]+) .* running on", line)

            if bootstrap_match:
                percentage = int(bootstrap_match.group(1))
                message = bootstrap_match.group(3)  # Get text after colon (:)

                print(f"{Fore.BLUE}Bootstrapped {percentage}% - {message}")

                if percentage == 100:
                    self.bootstrap_complete.set()  # Signal that bootstrap is complete

            # Always show bootstrap logs even if display_log is False
            elif self.config.display_log:
                if version_match:
                    version = version_match.group(1)
                    print(f"{Fore.YELLOW}Running Anon version {version}")

                elif error_match:
                    print(f"{Fore.RED}{line}")

                else:
                    print(f"{Style.DIM}{line}")
