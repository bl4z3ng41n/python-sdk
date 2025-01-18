from stem.control import Controller
from .exceptions import AnonError
from .models import Circuit, Relay
from typing import List, Optional


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
        Connect to the Anon control port or socket.
        Raises:
            AnonError: If the connection fails.
        """
        try:
            self.controller = Controller.from_port(port=self.control_port)
            self.controller.authenticate()
            print("Connected to the Control Port.")
        except Exception as e:
            raise AnonError(f"Failed to connect to the control port: {e}")

    def close(self):
        """
        Disconnect from the control port.
        """
        if self.controller:
            self.controller.close()
            self.controller = None
            print("Disconnected from the Control Port.")

    def get_circuits(self) -> List[Circuit]:
        """
        Fetch circuits from the control port.
        Returns:
            list: A list of structured circuits.
        """
        if not self.controller:
            raise AnonError("Not connected to the control port.")

        try:
            # Use Stem to get circuits
            circuit_events = self.controller.get_circuits()
            return self._format_circuits(circuit_events)  # Format the response
        except Exception as e:
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
            raise AnonError("Not connected to the control port.")

        try:
            circuits = self.get_circuits()
            for circuit in circuits:
                if circuit.id == circuit_id:
                    return circuit
            return None  # Circuit not found
        except Exception as e:
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
            raise AnonError("Not connected to the control port.")

        try:
            circuit_id = self.controller.extend_circuit(0, relays)
            return circuit_id
        except Exception as e:
            raise AnonError(f"Error creating circuit: {e}")

    def close_circuit(self, circuit_id: int):
        """
        Close an existing circuit.
        Args:
            circuit_id (int): The ID of the circuit to close.
        """
        if not self.controller:
            raise AnonError("Not connected to the control port.")

        try:
            self.controller.close_circuit(circuit_id)
        except Exception as e:
            raise AnonError(f"Error closing circuit {circuit_id}: {e}")
