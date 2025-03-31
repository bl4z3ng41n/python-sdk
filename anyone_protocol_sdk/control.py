from __future__ import annotations

from typing import List, Optional, Sequence, Tuple, Union, Mapping, Callable, Awaitable

import stem.control
from stem.descriptor.router_status_entry import RouterStatusEntryV3
from stem.response.events import CircuitEvent, StreamEvent, AddrMapEvent
from stem.descriptor.server_descriptor import RelayDescriptor

from .models import *


class Control():

    @staticmethod
    def from_port(address: str = '127.0.0.1', port: Union[int, str] = 'default') -> Control:
        return Control(stem.control.Controller.from_port(address, port))

    def __init__(self, controller: stem.control.Controller = None):
        self._controller = controller
        self._listener_map = {}

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

    def get_microdescriptor(self, relay: str) -> Microdescriptor:
        microdescriptor: Microdescriptor = self._controller.get_microdescriptor(
            relay)
        return self._to_microdescriptor(microdescriptor)

    def get_exit_policy(self, relay: str) -> stem.exit_policy.ExitPolicy:
        return self._controller.get_server_descriptor(relay).exit_policy

    def get_network_statuses(self, relays: Optional[Sequence[str]] = None) -> List[Relay]:
        router_statuses: List[RouterStatusEntryV3] = self._controller.get_network_statuses(
            relays)
        return self._to_relays(router_statuses)

    def get_streams(self) -> List[Stream]:
        stream_events: List[StreamEvent] = self._controller.get_streams()
        streams = self._to_streams(stream_events)
        return streams

    def get_stream(self, stream_id: int) -> Optional[Stream]:
        streams = self.get_streams()
        for stream in streams:
            if stream.id == stream_id:
                return stream
        return None

    def attach_stream(self, stream_id, circuit_id, exiting_hop=None):
        self._controller.attach_stream(stream_id, circuit_id, exiting_hop)

    def add_event_listener(self, listener: Callable[[Event], Union[None, Awaitable[None]]], eventType: EventType) -> None:

        def _wrapped_listener(event: stem.response.events.Event):
            wrapped_event = self._to_wrapped_event(event)
            listener(wrapped_event)

        listeners = self._listener_map[listener] if listener in self._listener_map else None
        if listeners:
            listeners.append(_wrapped_listener)
        else:
            self._listener_map[listener] = [_wrapped_listener]
        self._controller.add_event_listener(_wrapped_listener, eventType.name)

    def remove_event_listener(self, listener: Callable[[Event], Union[None, Awaitable[None]]]) -> None:
        listeners = self._listener_map[listener] if listener in self._listener_map else None
        if listeners:
            for _wrapped_listener in listeners:
                self._controller.remove_event_listener(_wrapped_listener)
            del self._listener_map[listener]

    def set_conf(self, param: str, value: Union[str, Sequence[str]]) -> None:
        self.set_options({param: value}, False)

    def reset_conf(self, params: str):
        self.set_options(Mapping([(entry, None) for entry in params]), True)

    def set_options(self, params: Union[Mapping[str, Union[str, Sequence[str]]], Sequence[Tuple[str, Union[str, Sequence[str]]]]], reset: bool = False) -> None:
        self._controller.set_options(params, reset)

    def get_info(self, params: Union[str, Sequence[str]]) -> Union[str, Mapping[str]]:
        return self._controller.get_info(params)

    def msg(self, message: str) -> str:
        return self._controller.msg(message)

    def resolve(self, address: str) -> str:
        return self.msg(f"RESOLVE {address}")

    def _to_microdescriptor(self, microdescriptor: stem.descriptor.microdescriptor) -> Microdescriptor:
        return Microdescriptor(
            onion_key=microdescriptor.onion_key,
            ntor_onion_key=microdescriptor.ntor_onion_key,
            or_addresses=microdescriptor.or_addresses,
            family=microdescriptor.family,
            exit_policy=microdescriptor.exit_policy,
            exit_policy_v6=microdescriptor.exit_policy_v6,
            identifiers=microdescriptor.identifiers,
            protocols=microdescriptor.protocols,
            digest=microdescriptor.digest(),
        )

    def _to_wrapped_event(self, event: stem.response.events.Event) -> Event:
        type = EventType[event.type]
        match type:
            case EventType.STREAM:
                try:
                    return self._to_stream(event)
                except AttributeError as e:
                    print(f"Failed to convert event to Stream: {e}")

            case EventType.ADDRMAP:
                return AddrMap(
                    type=type,
                    hostname=event.hostname,
                    destination=event.destination,
                    expiry=event.expiry,
                    error=event.error,
                    utc_expiry=event.utc_expiry,
                    cached=event.cached,
                )

            case EventType.WARN:
                return Log(
                    type=type,
                    message=event.message,
                )
            case EventType.INFO:
                return Log(
                    type=type,
                    message=event.message,
                )

            case _:
                return Event(
                    type=type,
                )

    def _to_circuits(self, circuit_events: List[CircuitEvent]) -> List[Circuit]:
        return [self._to_circuit(circuit_event) for circuit_event in circuit_events]

    def _to_circuit(self, circuit_event: CircuitEvent) -> Circuit:
        return Circuit(
            id=circuit_event.id,
            path=[self._to_hop(hop) for hop in circuit_event.path],
            created=circuit_event.created,
            status=CircuitStatus[circuit_event.status],
            purpose=CircuitPurpose[circuit_event.purpose],
        )

    def _to_hop(self, hop: Tuple[str, str]) -> Hop:
        return Hop(
            fingerprint=hop[0],
            nickname=hop[1],
        )

    def _to_relays(self, router_statuses: List[RouterStatusEntryV3]) -> List[Relay]:
        return [self._to_relay(router_status) for router_status in router_statuses]

    def _to_relay(self, router_status: RouterStatusEntryV3) -> Relay:
        return Relay(
            fingerprint=router_status.fingerprint,
            nickname=router_status.nickname,
            address=router_status.address,
            or_port=router_status.or_port,
            flags=[Flag[flag] for flag in router_status.flags],
            bandwidth=router_status.bandwidth,
            dir_port=router_status.dir_port,
            published=router_status.published,
            version_line=router_status.version_line,
            measured=router_status.measured,
            document=router_status.document,
            is_unmeasured=router_status.is_unmeasured,
            digest=router_status.digest,
            identifier=router_status.identifier,
            identifier_type=router_status.identifier_type,
            or_addresses=router_status.or_addresses,
            version=router_status.version,
            unrecognized_bandwidth_entries=router_status.unrecognized_bandwidth_entries,
            exit_policy=router_status.exit_policy,
            protocols=router_status.protocols,
            microdescriptor_hashes=router_status.microdescriptor_hashes,
        )

    def _to_streams(self, stream_events: List[StreamEvent]) -> List[Stream]:
        return [self._to_stream(stream_event) for stream_event in stream_events]

    def _to_stream(self, stream_event: StreamEvent) -> Stream:
        return Stream(
            type=EventType.STREAM,
            id=stream_event.id,
            target=stream_event.target,
            target_address=stream_event.target_address,
            target_port=stream_event.target_port,
            status=StreamStatus[stream_event.status],
            purpose=getattr(StreamPurpose, str(stream_event.purpose), None),
            circ_id=stream_event.circ_id,
            reason=stream_event.reason,
            remote_reason=stream_event.remote_reason,
            source=getattr(Source, str(stream_event.source), None),
            source_addr=stream_event.source_addr,
            source_address=stream_event.source_address,
            source_port=stream_event.source_port
        )

    # useful methods

    def is_accepted(self, address: str, port: int, relay: Relay) -> bool:
        print(f"Checking if relay {relay.nickname} can exit to {address}:{port}")
        try:
            exit_policy: stem.exit_policy.ExitPolicy = self.get_exit_policy(relay.fingerprint)
            if not exit_policy:
                print(
                    f"Relay defined as EXit but doesn't have any exit policy {relay.nickname}")
                return False
        except Exception as e:
            print(
                f"Failed to get exit policy descriptor for {relay.nickname}: {e}")
            return False

        return exit_policy.can_exit_to(address, port)

    def get_country(self, address: str) -> str:
        return self.get_info(f'ip-to-country/{address}')

    def disable_stream_attachment(self):
        self.set_conf('__LeaveStreamsUnattached', '1')

    def enable_stream_attachment(self):
        self.reset_conf('__LeaveStreamsUnattached')

    def disable_predicted_circuits(self):
        self.set_conf('__DisablePredictedCircuits', '1')

    def enable_predicted_circuits(self):
        self.reset_conf('__DisablePredictedCircuits')

    def get_relays(self) -> List[Relay]:
        return self.get_network_statuses()

    def get_relays_by_flags(self, flags: Union[str, Sequence[str]]) -> List[Relay]:
        relays = self.get_relays()
        return self.filter_relays_by_flags(relays, flags)

    def filter_relays_by_flags(self, relays: List[Relay], *flags: Flag) -> List[Relay]:
        return [relay for relay in relays if all(flag in relay.flags for flag in flags)]

    def get_relays_by_countries(self, countries: Union[str, Sequence[str]]) -> List[Relay]:
        relays = self.get_relays()
        return self.filter_relays_by_countries(relays, countries)

    def filter_relays_by_countries(self, relays: List[Relay], *countries: str) -> List[Relay]:
        return [relay for relay in relays if all(country in self.get_country(relay.address) for country in countries)]

    def get_circuits_with_relay_info_and_country(self):
        circuits = self.get_circuits()
        result = []
        for circuit in circuits:
            relays = []
            for hop in circuit.path:
                relay = self.get_network_status(hop.fingerprint)
                country = self.get_country(relay.address)
                relays.append({
                    'fingerprint': relay.fingerprint,
                    'nickname': relay.nickname,
                    'address': relay.address,
                    'country': country,
                    'or_port': relay.or_port,
                    'flags': relay.flags,
                    'bandwidth': relay.bandwidth,
                })
            result.append({
                'id': circuit.id,
                'created': circuit.created,
                'status': circuit.status,
                'purpose': circuit.purpose,
                'relays': relays
            })
        return result
