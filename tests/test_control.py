import unittest
from unittest.mock import MagicMock
from stem.control import Controller
from anon_python_sdk import Control


class TestControl(unittest.TestCase):

    def setUp(self):
        self.mock_controller = MagicMock(spec=Controller)
        self.control = Control(self.mock_controller)

    def test_authenticate(self):
        self.control.authenticate("password")
        self.mock_controller.authenticate.assert_called_with(
            "password", None, None)

    def test_close(self):
        self.control.close()
        self.mock_controller.close.assert_called_once()

    def test_new_circuit(self):
        self.mock_controller.extend_circuit.return_value = "2"
        circuit_id = self.control.new_circuit()
        self.assertEqual(circuit_id, "2")

    def test_attach_stream(self):
        self.control.attach_stream("1", "2")
        self.mock_controller.attach_stream.assert_called_with("1", "2", None)

    def test_set_conf(self):
        self.control.set_conf("MaxCircuitsPerConnection", "8")
        self.mock_controller.set_options.assert_called_with(
            {"MaxCircuitsPerConnection": "8"}, False)

    def test_get_info(self):
        self.mock_controller.get_info.return_value = "USA"
        country = self.control.get_country("1.1.1.1")
        self.assertEqual(country, "USA")


if __name__ == "__main__":
    unittest.main()
