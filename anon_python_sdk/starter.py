from anon_python_sdk import Control, Process, Config, Socks, StreamStatus, VPNConfig, Flag, EventType, Stream
import random


class Anon():
    def __init__(self):
        self.config = Config(
            auto_terms_agreement=True,
            display_log=False
        )
        self.anon = Process.launch_anon(anonrc_path=self.config.to_file())
        self.control = Control.from_port()
        self.socks = Socks()
        self.stream_listeners = []

    def start_vpn(self, country: str):
        self.control.authenticate()
        self.control.disable_predicted_circuits()
        relays = self.control.get_relays()
        nl_relays = self.control.filter_relays_by_countries(
            relays, country)
        exit_relays = self.control.filter_relays_by_flags(
            nl_relays, Flag.Exit)
        exit_relay_index = random.randint(0, len(exit_relays))
        exit = exit_relays[exit_relay_index].fingerprint
        guard_relays = self.control.filter_relays_by_flags(
            nl_relays, Flag.Guard)
        guard_relay_index = random.randint(0, len(guard_relays))
        guard = guard_relays[guard_relay_index].fingerprint
        path = [guard, exit]
        circuit_id = self.control.new_circuit(path=path, await_build=True)
        self.control.disable_stream_attachment()

        def attach_stream(stream: Stream):
            if stream.status == StreamStatus.NEW:
                self.control.attach_stream(stream.id, circuit_id)

        self.stream_listeners.append(attach_stream)
        self.control.add_event_listener(attach_stream, EventType.STREAM)

    def start_vpn_with_config(self, config: VPNConfig):
        self.control.authenticate()
        self.control.disable_stream_attachment()

        # map (target_address to circuit_id)
        self.routing_circuit_map = {}

        for routing in config.routings:
            relays = self.control.get_relays()
            nl_relays = self.control.filter_relays_by_countries(
                relays, *routing.exit_countries)
            exit_relays = self.control.filter_relays_by_flags(
                nl_relays, Flag.Exit)
            exit_relay_index = random.randint(0, len(exit_relays))
            exit = exit_relays[exit_relay_index].fingerprint
            guard_relays = self.control.filter_relays_by_flags(
                nl_relays, Flag.Guard)
            guard_relay_index = random.randint(0, len(guard_relays))
            guard = guard_relays[guard_relay_index].fingerprint
            path = [guard, exit]
            circuit_id = self.control.new_circuit(path=path, await_build=True)
            self.routing_circuit_map[routing.target_address] = circuit_id

        def attach_stream(stream: Stream):
            if stream.status == StreamStatus.NEW:
                self.control.attach_stream(
                    stream.id, self.routing_circuit_map[stream.target_address])

        self.stream_listeners.append(attach_stream)
        self.control.add_event_listener(attach_stream, EventType.STREAM)

    def stop_vpn(self):
        for listener in self.stream_listeners:
            self.control.remove_event_listener(listener)
        self.control.close()
        self.anon.stop()
