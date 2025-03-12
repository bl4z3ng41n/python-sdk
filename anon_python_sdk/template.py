from anon_python_sdk import Circuit, CircuitPurpose, CircuitBuildFlag, CircuitState, NodeSelectionFlag, Rule, Relay, Control, Flag
from typing import List
import random


def circuit_establish_circuit(purpose: CircuitPurpose, flags: List[CircuitBuildFlag], len: int = 3) -> Circuit:
    """Main function to establish a circuit."""

    state: CircuitState = CircuitState(
        need_capacity=CircuitBuildFlag.NEED_CAPACITY in flags,
        need_uptime=CircuitBuildFlag.NEED_UPTIME in flags,
        onehop_tunnel=CircuitBuildFlag.ONEHOP_TUNNEL in flags,
        is_internal=CircuitBuildFlag.IS_INTERNAL in flags,
        is_ipv6_selftest=CircuitBuildFlag.IS_IPV6_SELFTEST in flags,
        need_conflux=CircuitBuildFlag.NEED_CONFLUX in flags,
        desired_path_len=len,
    )

    circuit: Circuit = Circuit(purpose=purpose, state=state)

    circuit = populate_circuit_path(circuit)

    return circuit


def populate_circuit_path(circuit: Circuit) -> Circuit:
    r = 0

    while r == 0:
        r = onion_extend_cpath(circuit)

    return circuit


def onion_extend_cpath(circuit: Circuit) -> int:

    if circuit.state.desired_path_len >= len(circuit.path):
        return 1

    if len(circuit.path) == 0:
        r = choose_good_entry_server(circuit)

    elif len(circuit.path) == circuit.state.desired_path_len - 1:
        r = choose_good_exit_server(circuit)

    else:
        r = choose_good_middle_server(circuit)

    return 0


def choose_good_entry_server(circuit: Circuit) -> int:
    flags = [NodeSelectionFlag.CRN_DIRECT_CONN, NodeSelectionFlag.CRN_NEED_GUARD,
             NodeSelectionFlag.CRN_NEED_DESC, NodeSelectionFlag.CRN_PREF_ADDR]

    rule = Rule.WEIGHT_FOR_GUARD

    choise = choose_random_node(circuit, flags, rule)

    return


def choose_good_exit_server(circuit: Circuit) -> int:
    pass
    return 0


def choose_good_middle_server(circuit: Circuit) -> int:
    pass
    return 0


def choose_random_node(control: Control, circuit: Circuit, flags: List[NodeSelectionFlag], rule: Rule) -> Relay:
    # control = Control.from_port()
    # control.authenticate()

    relays = control.get_relays()

    if NodeSelectionFlag.CRN_NEED_GUARD in flags:
        filtered = [
            relay for relay in relays
            if Flag.Guard in relay.flags
        ]

    if not filtered:
        return None

    total_bandwidth = sum(relay.bandwidth for relay in filtered)

    probabilities = [relay.bandwidth / total_bandwidth for relay in filtered]
    chosen_relay = random.choices(filtered, weights=probabilities, k=1)[0]

    return chosen_relay
