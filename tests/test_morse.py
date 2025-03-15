"""Testing the morse class"""

from unittest.mock import Mock, call

from morse.morse import Morse


def test_send_message_e():
    transmitter = Mock()
    morse = Morse(transmitter)
    morse.send_message("e")

    transmitter.transmit.assert_called_once_with(0)


def test_send_message_a():
    transmitter = Mock()
    morse = Morse(transmitter)
    morse.send_message("a")

    expected_calls = [call(0), call(1)]
    transmitter.transmit.assert_has_calls(expected_calls)
