from __future__ import annotations

from typing import List, Optional, Sequence, Tuple, Union

import stem.control
from stem.descriptor.router_status_entry import RouterStatusEntryV3
from stem.response.events import CircuitEvent

from .models import Circuit, Hop, Relay


class Control():

    @staticmethod
    def from_port(address: str = '127.0.0.1', port: Union[int, str] = 'default') -> Control:
        return Control(stem.control.Controller.from_port(address, port))

    def __init__(self, controller: stem.control.Controller = None):
        self._controller = controller

    def authenticate(self, password=None, chroot_path=None, protocolinfo_response=None):
        self._controller.authenticate(
            password, chroot_path, protocolinfo_response)

    def close(self):
        self._controller.close()

    def get_circuits(self) -> List[Circuit]:
        circuit_events: List[CircuitEvent] = self._controller.get_circuits()
        circuits = self._to_circuits(circuit_events)
        return circuits

    def get_circuit(self, circuit_id: int) -> Optional[Circuit]:
        circuits = self.get_circuits()
        for circuit in circuits:
            if circuit.id == circuit_id:
                return circuit
        return None

    def new_circuit(self, path: Union[None, str, Sequence[str]] = None, purpose: str = 'general', await_build: bool = False, timeout: Optional[float] = None) -> str:
        return self.extend_circuit('0', path, purpose, await_build, timeout)

    def extend_circuit(self, circuit_id: str = '0', path: Union[None, str, Sequence[str]] = None, purpose: str = 'general', await_build: bool = False, timeout: Optional[float] = None) -> str:
        return self._controller.extend_circuit(circuit_id, path, purpose, await_build, timeout)

    def close_circuit(self, circuit_id: str, flag: str = '') -> None:
        return self._controller.close_circuit(circuit_id, flag)

    def get_network_status(self, relay: Optional[str] = None) -> Relay:
        router_status: RouterStatusEntryV3 = self._controller.get_network_status(
            relay)
        return self._to_relay(router_status)

    def get_country(self, address: Optional[str] = None) -> str:
        return self._controller.get_info(f'ip-to-country/{address}')

    def _to_circuits(self, circuit_events: List[CircuitEvent]) -> List[Circuit]:
        return [self._to_circuit(circuit_event) for circuit_event in circuit_events]

    def _to_circuit(self, circuit_event: CircuitEvent) -> Circuit:
        return Circuit(
            id=circuit_event.id,
            path=[self._to_hop(hop) for hop in circuit_event.path],
            created=circuit_event.created,
        )

    def _to_hop(self, hop: Tuple[str, str]) -> Hop:
        return Hop(
            fingerprint=hop[0],
            nickname=hop[1],
        )

    def _to_relay(self, router_status: RouterStatusEntryV3) -> Relay:
        return Relay(
            fingerprint=router_status.fingerprint,
            nickname=router_status.nickname,
            address=router_status.address,
            or_port=router_status.or_port,
            flags=router_status.flags,
            bandwidth=router_status.bandwidth,
        )
