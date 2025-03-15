"""Test module for the Morse class.

This module contains unit tests for the Morse class functionality, specifically testing
message transmission using a mock transmitter.

Tests:
    test_send_message_e: Tests transmission of the letter 'e' in Morse code
    test_send_message_a: Tests transmission of the letter 'a' in Morse code
"""

from unittest.mock import Mock, call

from morse.morse import Morse


def test_send_message_e():
    """Test sending the letter 'e' in Morse code."""
    transmitter = Mock()
    morse = Morse(transmitter)
    morse.send_message("e")

    transmitter.transmit.assert_called_once_with(0)


def test_send_message_a():
    """Test sending the letter 'a' in Morse code."""
    transmitter = Mock()
    morse = Morse(transmitter)
    morse.send_message("a")

    expected_calls = [call(0), call(1)]
    transmitter.transmit.assert_has_calls(expected_calls)
