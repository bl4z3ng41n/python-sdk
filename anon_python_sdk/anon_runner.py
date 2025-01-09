import subprocess
import platform
from pathlib import Path

# Path to the binary directory and default anonrc file
BINARY_DIR = Path.home() / ".anon-python-sdk" / "bin"
DEFAULT_ANONRC = Path("/usr/local/etc/anon") / "anonrc"

# Platform-specific binary names
PLATFORM_MAP = {
    "linux": "anon",
    "darwin": "anon",
    "windows": "anon.exe",
}

def get_binary_path():
    """
    Determine the path to the Anon binary based on the platform.
    Returns:
        Path: Path to the binary file.
    Raises:
        OSError: If the platform is unsupported or the binary is missing.
    """
    system = platform.system().lower()
    binary_name = PLATFORM_MAP.get(system)
    if not binary_name:
        raise OSError(f"Unsupported platform: {system}")
    
    binary_path = BINARY_DIR / binary_name
    if not binary_path.is_file():
        raise FileNotFoundError(f"Anon binary not found: {binary_path}")
    
    return binary_path

def get_anonrc_path(custom_anonrc=None):
    """
    Get the path to the anonrc configuration file.
    Args:
        custom_anonrc (Path, optional): Path to a custom anonrc file.
    Returns:
        Path: Path to the anonrc file to use.
    """
    return custom_anonrc if custom_anonrc else DEFAULT_ANONRC

def start_anon(custom_anonrc=None):
    """
    Start the Anon process with the specified anonrc file.
    Args:
        custom_anonrc (Path, optional): Path to a custom anonrc file.
    Returns:
        int: The process ID of the started Anon process.
    """
    binary_path = get_binary_path()
    anonrc_path = get_anonrc_path(custom_anonrc)
    
    if not anonrc_path.is_file():
        raise FileNotFoundError(f"anonrc file not found: {anonrc_path}")
    
    process = subprocess.Popen([str(binary_path), "-f", str(anonrc_path)])
    print(f"Anon started with PID: {process.pid}, using anonrc: {anonrc_path}")
    return process.pid

def stop_anon(pid):
    """
    Stop the Anon process by its PID.
    Args:
        pid (int): Process ID of the Anon process to stop.
    """
    try:
        subprocess.check_call(["kill", "-9", str(pid)])
        print(f"Anon process with PID {pid} stopped.")
    except Exception as e:
        print(f"Failed to stop process {pid}: {e}")

def create_default_anonrc():
    """
    Create a default anonrc file if it doesn't exist.
    """
    if not DEFAULT_ANONRC.is_file():
        DEFAULT_ANONRC.parent.mkdir(parents=True, exist_ok=True)
        with open(DEFAULT_ANONRC, "w") as f:
            f.write("# Default anonrc for Anon\n")
            f.write("SocksPort 9050\n")
            f.write("ControlPort 9051\n")
        print(f"Default anonrc created at {DEFAULT_ANONRC}")

