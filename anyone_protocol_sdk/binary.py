from pathlib import Path
import platform

# Path to the binary directory and default anonrc file
BINARY_DIR = Path.home() / ".anyone_protocol_sdk" / "bin"

# Platform-specific binary names
PLATFORM_MAP = {
    "linux": "anon",
    "darwin": "anon",
    "windows": "anon.exe",
}


def get_binary_path() -> str:
    """
    Determine the path to the Anon binary based on the platform.
    """
    system = platform.system().lower()
    binary_name = PLATFORM_MAP.get(system)

    if not binary_name:
        raise OSError(f"Unsupported platform: {system}")

    binary_path = (BINARY_DIR / binary_name)
    if not binary_path.exists():
        raise FileNotFoundError(
            f"Anon binary not found at: {binary_path}")

    return str(binary_path)
