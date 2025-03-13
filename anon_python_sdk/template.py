from anon_python_sdk import Circuit, CircuitPurpose, CircuitBuildFlag, CircuitBuildState, Relay, Control, Flag
from typing import List
import random


def build_circuit_path(control: Control, desired_exit_countries: List[str] = [], len: int = 2) -> List[Relay]:
    state: CircuitBuildState = CircuitBuildState(
        desired_path_len=len,
        excluded_nodes=[],
        excluded_countries=[],
        desired_exit_countries=[country.lower()
                                for country in desired_exit_countries],
        path=[]
    )

    state = _populate_circuit_path(control, state)

    return state.path


def _populate_circuit_path(control: Control, state: CircuitBuildState) -> CircuitBuildState:
    print("Populating circuit path")
    r = 0

    while r == 0:
        r = _onion_extend_cpath(control, state)

    return state


def _onion_extend_cpath(control: Control, state: CircuitBuildState) -> int:
    print("Extending circuit path")
    print(f"Current path length: {len(state.path)}")
    print(f"Desired path length: {state.desired_path_len}")
    if len(state.path) >= state.desired_path_len:
        return 1

    if len(state.path) == 0:
        print("Choosing entry server")
        relay = _choose_good_entry_server(control, state)

    elif len(state.path) == state.desired_path_len - 1:
        print("Choosing exit server")
        relay = _choose_good_exit_server(control, state)

    else:
        print("Choosing middle server")
        relay = _choose_good_middle_server(control, state)

    try:
        md = control.get_microdescriptor(relay.fingerprint)
        state.path.append(relay)
        print("Excluding relay", relay.nickname)
        state.excluded_nodes.append(relay.fingerprint)
        state.excluded_nodes.extend(md.family)
        country = control.get_country(relay.address)
        print("Exclude country: ", country)
        state.excluded_countries.append(country)
    except Exception as e:
        print(
            f"Failed to get microdescriptor for {relay.nickname}: {e}. Exclude relay.")
        state.excluded_nodes.append(relay.fingerprint)

    return 0


def _choose_good_entry_server(control: Control, state: CircuitBuildState) -> Relay:
    relays = control.get_relays()

    filtered = [
        relay for relay in relays
        if Flag.Guard in relay.flags and relay.fingerprint not in state.excluded_nodes
    ]

    filteredOut = [
        relay for relay in filtered
        if control.get_country(relay.address) not in state.excluded_countries
    ]

    filteredIn = [
        relay for relay in filteredOut
        if control.get_country(relay.address) not in state.desired_exit_countries
    ]

    filtered = len(filteredIn) > 0 and filteredIn or filteredOut

    return _choose_random_node(filtered)


def _choose_good_exit_server(control: Control, state: CircuitBuildState) -> Relay:
    print("Choosing exit server")
    relays = control.get_relays()

    filtered = [
        relay for relay in relays
        if Flag.Exit in relay.flags and Flag.BadExit not in relay.flags and relay.fingerprint not in state.excluded_nodes
    ]

    print(f"Filtered Exit 1: {len(filtered)}")

    # filter out excluded countries, filter in desired exit countries

    filteredOut = [
        relay for relay in filtered
        if control.get_country(relay.address) not in state.excluded_countries
    ]

    filteredIn = [
        relay for relay in filteredOut
        if control.get_country(relay.address) in state.desired_exit_countries
    ]

    filtered = len(filteredIn) > 0 and filteredIn or filteredOut

    print(f"Filtered Exit 2: {len(filteredIn)}")

    return _choose_random_node(filtered)


def _choose_good_middle_server(control: Control, state: CircuitBuildState) -> int:
    pass
    return 0


def _choose_random_node(relays: List[Relay]) -> Relay:
    print(f"Choosing from {len(relays)} relays")
    total_bandwidth = sum(relay.bandwidth for relay in relays)

    probabilities = [relay.bandwidth / total_bandwidth for relay in relays]
    chosen_relay = random.choices(relays, weights=probabilities, k=1)[0]
    print(f"Chose relay: {chosen_relay.nickname}")
    return chosen_relay
