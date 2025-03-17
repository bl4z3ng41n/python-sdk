from anon_python_sdk import *
from typing import List, Optional
import random


def find_or_create_circuit(control: Control, stream: Stream) -> Optional[str]:

    circuits = control.get_circuits()

    print(f"Found {len(circuits)} circuits")
    print(f"Stream status: {stream.status}. Purpose: {stream.purpose}")

    if stream.status != StreamStatus.NEW:
        print("Stream is not new")
        return None

    print(f"Found {len(circuits)} circuits")

    filtered = [
        circuit for circuit in circuits
        if circuit.purpose in [CircuitPurpose.GENERAL, CircuitPurpose.CONTROLLER] and circuit.status in [CircuitStatus.BUILT, CircuitStatus.EXTENDED]
    ]

    print(f"Filtered {len(filtered)} circuits")

    if stream.purpose != StreamPurpose.USER:
        print("Stream is not for user")
        return random.choice(filtered).id

    # filte out circuits which has no exit relay or exit relay is not supporting exit policy

    filtered = [
        circuit for circuit in filtered
        if _is_circuit_exit_relay_has_good_exit_policy(control, circuit, stream)
    ]

    print(f"Filtered with good exit policy {len(filtered)} circuits")

    # get random circuit from filtered circuits
    if len(filtered) == 0:
        # close all circuits
        print("Closing all circuits")
        for circuit in circuits:
            control.close_circuit(circuit.id)
        print("All circuits closed")

        circuit_id = None
        while not circuit_id:
            pathRelays = build_circuit_path(control, [], 2)

            try:
                md = control.get_microdescriptor(pathRelays[-1].fingerprint)
                exit_policy = control.get_exit_policy(
                    pathRelays[-1].fingerprint)
                print("Exit desc policy:", md.exit_policy)
                print("Exit info:", pathRelays[-1])
                print("Exit policy:", exit_policy)
                print("------------------------------------")
                path = [pathRelays[0].fingerprint, pathRelays[1].fingerprint]
                circuit_id = control.new_circuit(
                    path=path, await_build=True, timeout=5)
                print("Created circuit", circuit_id)
            except Exception as e:
                print(
                    f"Failed to get microdescriptor for {pathRelays[1].nickname}:{e}")

        return circuit_id

    circuit = None

    while not circuit:
        try:
            circuit = random.choice(filtered)
            exit_info = control.get_network_status(
                circuit.path[-1].fingerprint)
            md = control.get_microdescriptor(circuit.path[-1].fingerprint)
            exit_policy = control.get_exit_policy(circuit.path[-1].fingerprint)

            print("Exit desc policy:", md.exit_policy)
            print("Exit info:", exit_info)
            print("Exit policy:", exit_policy)
        except Exception as e:
            print(
                f"Failed to get microdescriptor for {circuit.path[-1].nickname}:{e}")
            circuit = None

    return circuit.id


def _is_circuit_exit_relay_has_good_exit_policy(control: Control, circuit: Circuit, stream: Stream) -> bool:
    if len(circuit.path) == 0:
        return False

    exit_relay = circuit.path[-1]

    try:
        md = control.get_microdescriptor(exit_relay.fingerprint)
    except Exception as e:
        print(f"Failed to get microdescriptor for {exit_relay.nickname}: {e}")
        return False

    # get relay info
    relay = control.get_network_status(exit_relay.fingerprint)

    # does exit relay has exit flag and has no bad exit flag
    if Flag.Exit not in relay.flags or Flag.BadExit in relay.flags:
        return False

    # for now just use random
    return True


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
    print("Circuit path built:", state.path)

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

    # filter in stable, valid, running, fast

    filtered = [
        relay for relay in relays
        if Flag.Stable in relay.flags and Flag.Valid in relay.flags and Flag.Running in relay.flags and Flag.Fast in relay.flags
    ]

    filtered = [
        relay for relay in filtered
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

    # filtered = [
    #     relay for relay in relays
    #     if Flag.Stable in relay.flags and Flag.Valid in relay.flags and Flag.Running in relay.flags and Flag.Fast in relay.flags
    # ]

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
