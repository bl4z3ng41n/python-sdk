from __future__ import annotations
from typing import Callable, Dict, Optional, Sequence, Union
from anyone_protocol_sdk.binary import get_binary_path

import subprocess
import stem.process
import re


DEFAULT_CMD = get_binary_path()
DEFAULT_INIT_TIMEOUT = 90
DEFAULT_COMPLETION_PERCENT = 100


# temporary here
def default_init_msg_handler(line: str, display_log: bool = False):
    line = line.strip()

    bootstrap_match = re.search(
        r"Bootstrapped (\d+)% \(([^)]+)\): (.+)", line)
    error_match = re.search(r"\[err\]", line, re.IGNORECASE)
    version_match = re.search(
        r"Anon (\d+\.\d+\.\d+[\w.-]+) .* running on", line)

    if bootstrap_match:
        percentage = int(bootstrap_match.group(1))
        message = bootstrap_match.group(3)
        print(f"Bootstrapped {percentage}% - {message}")

    if display_log:
        if version_match:
            version = version_match.group(1)
            print(f"Running Anon version {version}")
        elif error_match:
            print(f"{line}")
        else:
            print(f"{line}")


class Process:

    def __init__(self, process: subprocess.Popen):
        self._process = process

    @staticmethod
    def launch_anon(anon_cmd: str = DEFAULT_CMD, args: Optional[Sequence[str]] = None, anonrc_path: Optional[str] = None, completion_percent: int = DEFAULT_COMPLETION_PERCENT, init_msg_handler: Optional[Callable[[str], None]] = default_init_msg_handler, timeout: int = DEFAULT_INIT_TIMEOUT, take_ownership: bool = False, close_output: bool = True, stdin: Optional[str] = None) -> Process:
        return Process(stem.process.launch_tor(anon_cmd, args, anonrc_path, completion_percent, init_msg_handler, timeout, take_ownership, close_output, stdin))

    @staticmethod
    def launch_anon_with_config(config: Dict[str, Union[str, Sequence[str]]], anon_cmd: str = DEFAULT_CMD, completion_percent: int = DEFAULT_COMPLETION_PERCENT, init_msg_handler: Optional[Callable[[str], None]] = default_init_msg_handler, timeout: int = DEFAULT_INIT_TIMEOUT, take_ownership: bool = False, close_output: bool = True) -> Process:
        return Process(stem.process.launch_tor_with_config(config, anon_cmd, completion_percent, init_msg_handler, timeout, take_ownership, close_output))

    def stop(self):
        if self._process and self._process.poll() is None:
            print(f"Stopping Anon process with PID: {self._process.pid}")
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
                print(f"Anon process terminated gracefully")
            except subprocess.TimeoutExpired:
                print(f"Anon process did not stop. Killing it...")
                self._process.kill()
                self._process.wait()
                print(f"Anon process killed")
        else:
            print(f"Anon process is not running")
