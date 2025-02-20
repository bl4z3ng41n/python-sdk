from anon_python_sdk import Control, Process, Config, Socks


class Anon():
    def __init__(self):
        self.config = Config(
            auto_terms_agreement=True,
            display_log=False
        )
        self.anon = Process.launch_anon(anonrc_path=self.config.to_file())
        self.control = Control.from_port()
        self.socks = Socks()

    def start_vpn(self, country: str):
        self.control.authenticate()
        relays = self.control.get_relays()
        nl_relays = self.control.filter_relays_by_countries(
            relays, country)
        exit_relays = self.control.filter_relays_by_flags(
            nl_relays, "Exit")
        exit = exit_relays[0].fingerprint
        guard_relays = self.control.filter_relays_by_flags(
            nl_relays, "Guard")
        guard = guard_relays[0].fingerprint
        path = [guard, exit]
        circuit_id = self.control.new_circuit(path=path, await_build=True)
        self.control.disable_stream_attachment()

        def attach_stream(stream):
            if stream.status == 'NEW':
                self.control.attach_stream(stream.id, circuit_id)

        self.stream_listener = attach_stream
        self.control.add_event_listener(attach_stream)

    def stop_vpn(self):
        self.control.remove_event_listener(self.stream_listener)
        self.control.close()
        self.anon.stop()
