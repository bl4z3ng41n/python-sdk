from stem.control import Controller
from .exceptions import AnonError
from .models import Circuit, Relay, RelayInfo
from typing import List, Optional
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

class ControlClient:
    """
    A client to interact with the Anon control port.
    """

    def __init__(self, control_port=9051):
        """
        Initialize the ControlClient.
        Args:
            control_port (int): The control port to connect to (default: 9051).
        """
        self.control_port = control_port
        self.controller = None

    def connect(self):
        """
        Connect to the Anon control port.
        Raises:
            AnonError: If the connection fails.
        """
        try:
            self.controller = Controller.from_port(port=self.control_port)
            self.controller.authenticate()
            print(f"{Fore.GREEN}Connected to the Control Port (Port: {self.control_port}).")
        except Exception as e:
            print(f"{Fore.RED}Failed to connect to the control port: {e}")
            raise AnonError(f"Failed to connect to the control port: {e}")

    def close(self):
        """
        Disconnect from the control port.
        """
        if self.controller:
            self.controller.close()
            self.controller = None
            print(f"{Fore.YELLOW}Disconnected from the Control Port.")

    def get_circuits(self) -> List[Circuit]:
        """
        Fetch circuits from the control port.
        Returns:
            list: A list of structured circuits.
        """
        if not self.controller:
            raise AnonError(f"{Fore.RED}Not connected to the control port. Please call 'connect()' first.")

        try:
            print(f"{Fore.BLUE}Fetching circuits...")
            circuit_events = self.controller.get_circuits()
            circuits = self._format_circuits(circuit_events)
            print(f"{Fore.GREEN}Retrieved {len(circuits)} circuits.")
            return circuits
        except Exception as e:
            print(f"{Fore.RED}Error fetching circuits: {e}")
            raise AnonError(f"Error fetching circuits: {e}")
    
    def _format_circuits(self, circuit_events) -> List[Circuit]:
        formatted_circuits = []
        for circuit in circuit_events:
            formatted_circuits.append(
                Circuit(
                    id=circuit.id,
                    status=circuit.status,
                    path=[
                        Relay(
                            fingerprint=relay[0],
                            nickname=relay[1] if len(relay) > 1 else None,
                        )
                        for relay in circuit.path
                    ],
                    purpose=getattr(circuit, "purpose", None),
                    time_created=getattr(circuit, "time_created", None),
                )
            )
        return formatted_circuits
    
    def get_circuit(self, circuit_id: int) -> Optional[Circuit]:
        """
        Fetch a specific circuit by its ID.
        Args:
            circuit_id (int): The ID of the circuit to fetch.
        Returns:
            Optional[Circuit]: The Circuit object if found, or None if the circuit doesn't exist.
        """
        if not self.controller:
            raise AnonError(f"{Fore.RED}Not connected to the control port. Please call 'connect()' first.")

        try:
            circuits = self.get_circuits()
            for circuit in circuits:
                if circuit.id == circuit_id:
                    print(f"{Fore.GREEN}Found circuit {circuit_id}.")
                    return circuit
            print(f"{Fore.YELLOW}Circuit {circuit_id} not found.")
            return None
        except Exception as e:
            print(f"{Fore.RED}Error fetching circuit {circuit_id}: {e}")
            raise AnonError(f"Error fetching circuit {circuit_id}: {e}")
    
    def create_circuit(self, relays: List[str] = None) -> int:
        """
        Create a new circuit through the specified relays.
        Args:
            relays (List[str]): A list of relay fingerprints or nicknames.
        Returns:
            int: The ID of the newly created circuit.
        """
        if not self.controller:
            raise AnonError(f"{Fore.RED}Not connected to the control port. Please call 'connect()' first.")

        try:
            circuit_id = self.controller.extend_circuit(0, relays)
            print(f"{Fore.GREEN}Successfully created circuit {circuit_id}.")
            return circuit_id
        except Exception as e:
            print(f"{Fore.RED}Error creating circuit: {e}")
            raise AnonError(f"Error creating circuit: {e}")

    def close_circuit(self, circuit_id: int):
        """
        Close an existing circuit.
        Args:
            circuit_id (int): The ID of the circuit to close.
        """
        if not self.controller:
            raise AnonError(f"{Fore.RED}Not connected to the control port. Please call 'connect()' first.")

        try:
            self.controller.close_circuit(circuit_id)
            print(f"{Fore.GREEN}Successfully closed circuit {circuit_id}.")
        except Exception as e:
            print(f"{Fore.RED}Error closing circuit {circuit_id}: {e}")
            raise AnonError(f"Error closing circuit {circuit_id}: {e}")

    def get_relay_info(self, fingerprint: str) -> RelayInfo:
        """
        Get relay information by fingerprint.

        Args:
            fingerprint (str): The relay fingerprint.

        Returns:
            RelayInfo: Relay information as a structured object.
        """
        if not self.controller:
            raise AnonError(f"{Fore.RED}Control client is not connected. Call 'connect()' first.")

        try:
            print(f"{Fore.BLUE}Fetching relay info for fingerprint: {fingerprint}...")
            response = self.controller.get_info(f"ns/id/${fingerprint}")
        except Exception as e:
            print(f"{Fore.RED}Failed to fetch relay info for {fingerprint}: {e}")
            raise AnonError(f"Failed to fetch relay info for {fingerprint}: {e}")

        # Parse the response
        lines = response.splitlines()
        nickname, ip, or_port, flags, bandwidth = "", "", 0, [], 0

        for line in lines:
            line = line.strip()

            if line.startswith("s "):  # Flags
                flags = line[2:].strip().split(" ")

            elif line.startswith("r "):  # IP, ORPort, Nickname
                parts = line.split(" ")
                if len(parts) >= 8:
                    nickname = parts[1]
                    ip = parts[6]
                    or_port = int(parts[7])

            elif line.startswith("w "):  # Bandwidth
                bandwidth = int(line.split("=")[1])

        print(f"{Fore.GREEN}Retrieved relay info for {fingerprint}: {nickname}, IP: {ip}, ORPort: {or_port}.")
        
        return RelayInfo(
            fingerprint=fingerprint,
            nickname=nickname,
            ip=ip,
            or_port=or_port,
            flags=flags,
            bandwidth=bandwidth,
        )
