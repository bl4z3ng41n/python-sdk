from anon_python_sdk import Config, Process, Control, choose_random_node, Circuit, NodeSelectionFlag, Rule

# Create a configuration
config = Config(
    auto_terms_agreement=True,
    display_log=True,
)

anon = Process.launch_anon(anonrc_path=config.to_file())

control = Control.from_port()

try:

    control.authenticate()

    relay = choose_random_node(
        control, None, [NodeSelectionFlag.CRN_NEED_GUARD], Rule.WEIGHT_FOR_GUARD)

    print(relay)


except Exception as e:
    print(f"Anon failed to start: {e}")
finally:
    anon.stop()
    print("Anon has stopped.")
