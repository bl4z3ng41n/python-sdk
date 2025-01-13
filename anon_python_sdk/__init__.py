"""
Anon Python SDK

This package provides tools to interact with the Anon network, including:
- Managing the Anon process (start/stop).
- Configuring and managing circuits.
- Fetching relay information and more.

Quick Start:
    from anon_python_sdk import start_anon, stop_anon

    # Start the Anon process
    pid = start_anon()

    # Stop the Anon process
    stop_anon(pid)
"""

# Import key functions and classes for top-level access
from .anon_runner import start_anon, stop_anon, create_default_anonrc
from .control_client import ControlClient
from .exceptions import AnonError

__all__ = ["ControlClient", "Circuit", "Relay", "AnonError"]
