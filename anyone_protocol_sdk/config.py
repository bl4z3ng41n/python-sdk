import os
import tempfile
from pathlib import Path
from typing import Optional, List
from datetime import datetime


class Config:
    """
    Configuration object for the Anon binary.
    """

    def __init__(
            self,
            display_log: Optional[bool] = True,
            use_exec_file: Optional[bool] = False,
            socks_port: int = 9050,
            or_port: int = 0,  # Disable by default
            control_port: int = 9051,
            config_file: Optional[str] = None,
            binary_path: Optional[str] = None,
            auto_terms_agreement: Optional[bool] = False,
            exit_countries: Optional[List[str]] = None,
    ):
        self.display_log = display_log
        self.use_exec_file = use_exec_file
        self.socks_port = socks_port
        self.or_port = or_port
        self.control_port = control_port
        self.config_file = config_file
        self.binary_path = binary_path
        self.auto_terms_agreement = auto_terms_agreement
        self.exit_countries = exit_countries

    def to_dict(self):
        """
        Converts the configuration to a dictionary format.
        """
        return {
            "display_log": self.display_log,
            "use_exec_file": self.use_exec_file,
            "socks_port": self.socks_port,
            "or_port": self.or_port,
            "control_port": self.control_port,
            "config_file": self.config_file,
            "binary_path": self.binary_path,
            "auto_terms_agreement": self.auto_terms_agreement,
            "exit_countries": self.exit_countries,
        }

    def to_file(self) -> str:
        """
        Creates an Anon configuration file and returns its path.
        If a config file is provided and exists, it will be reused.
        """

        # Use existing config file if provided and accessible
        if self.config_file:
            config_path = Path(self.config_file)
            if config_path.exists():
                print(f"Using existing Anon config: {config_path}")
                return str(config_path)

        # Create a subdirectory in the temp directory for Anon
        temp_dir = Path(tempfile.gettempdir()) / "anon"
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique directory and config file names
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        temp_data_dir_path = temp_dir / f"anon-data-{timestamp}"
        config_path = temp_data_dir_path / f"anonrc-{timestamp}.conf"

        # Create data directory
        temp_data_dir_path.mkdir(parents=True, exist_ok=True)

        # Create configuration items
        config_items = [
            f"DataDirectory {temp_data_dir_path}",
            f"SOCKSPort {self.socks_port}",
            f"ORPort {self.or_port}",
            f"ControlPort {self.control_port}",
            f"Log info stdout",
        ]

        # Handle exit nodes if specified
        if self.exit_countries:
            exit_nodes = ",".join(
                f"{{{country.upper()}}}" for country in self.exit_countries)
            config_items.append(f"ExitNodes {exit_nodes}")
            print(f"Using Exit Nodes: {exit_nodes}")

        # Handle automatic terms agreement
        if self.auto_terms_agreement:
            config_items.append("AgreeToTerms 1")
        else:
            terms_agreement_file = Path(os.getcwd()) / "terms-agreement"
            if not check_terms_agreement(terms_agreement_file):
                if ask_for_agreement():
                    print(f"Terms agreement accepted.")
                    terms_agreement_file.write_text("agreed")
                else:
                    print(f"Agreement declined. Exiting...")
                    exit(1)

        # Write to configuration file inside the data directory
        try:
            with open(config_path, "w") as f:
                f.write("\n".join(config_items) + "\n")
        except Exception as e:
            print(f"Failed to create config file: {e}")
            raise

        return str(config_path)


def ask_for_agreement() -> bool:
    """
    Prompt the user for agreement to terms.
    """
    try:
        print(f"Do you agree to the terms? (Press Enter or 'y' to agree, or Ctrl+C to exit): ", end="")
        agreement = input().strip().lower()
        return agreement in {"y", ""}
    except KeyboardInterrupt:
        print(f"\nAgreement declined. Exiting...")
        exit(1)


def check_terms_agreement(file_path: Path) -> bool:
    """
    Check if the terms agreement file contains the word 'agreed'.
    """
    if file_path.exists():
        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
                return content == "agreed"
        except Exception as e:
            print(f"Error reading terms agreement file: {e}")
    return False
