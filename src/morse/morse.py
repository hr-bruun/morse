"""Module providing classes for timing and transmitting morse code."""

from abc import ABC, abstractmethod
import time
from typing import List

from .alphabet import ALPHABET

class Transmitter(ABC):
    """An abstract transmitter class."""

    @abstractmethod
    def transmit(self, dot_or_dash: int) -> None:
        """Transmit a dot or dash."""
        pass

    @abstractmethod
    def end_of_word(self) -> None:
        """Handle end of word."""
        pass

    @abstractmethod
    def end_of_character(self) -> None:
        """Handle end of character."""
        pass


class Morse:  # pylint: disable=too-few-public-methods
    """Class representing a morse code sender"""

    def __init__(self, transmitter: Transmitter):
        self.transmitter = transmitter

    def send_message(self, message: str) -> None:
        """Send a morse code message."""
        for letter in message.lower():
            self._send_letter(letter)
        self._send_letter(" ")

    def _send_letter(self, letter: str) -> None:
        """Send a single letter in morse code."""
        if letter == " ":
            self.transmitter.end_of_word()
        else:
            for dot_or_dash in ALPHABET[letter]:
                self.transmitter.transmit(dot_or_dash)
            self.transmitter.end_of_character()

class ParisTimer:
    """A morse code timer using Paris timing."""

    INTER_WORD_PAUSE = 7

    def __init__(self, wpm: int):
        self.dit_length = ParisTimer.calculate_dit_length(wpm)

    def end_of_word(self) -> None:
        """Pause at the end of a word."""
        self._pause(self.INTER_WORD_PAUSE)

    def end_of_character(self) -> None:
        """Pause at the end of a character."""
        self._pause(2)  # Makes 3 in all for inter-character space

    def end_of_dot_or_dash(self) -> None:
        """Pause at the end of a dot or dash."""
        self._pause(1)  # intra-character space

    def dot_or_dash(self, dot_or_dash: int) -> None:
        """Transmit a dot or dash."""
        self._pause(1 if dot_or_dash == 0 else 3)

    def _pause(self, units: int) -> None:
        """Pause for a given number of units."""
        time.sleep(units * self.dit_length)

    @staticmethod
    def calculate_dit_length(wpm: int) -> float:
        """Calculate the length of a dit based on words per minute."""
        # Using the "PARIS" standard word (50 units long)
        return 60 / (50 * wpm)


class DebugTransmitter(Transmitter):
    """A debug transmitter."""

    def __init__(self, timer: ParisTimer):
        self.timer = timer

    def transmit(self, dot_or_dash: int) -> None:
        """Transmit a dot or dash."""
        print("." if dot_or_dash == 0 else "-", end="")
        self.timer.dot_or_dash(dot_or_dash)
        self.timer.end_of_dot_or_dash()

    def end_of_character(self) -> None:
        """Handle end of character."""
        print("/", end=" ")
        self.timer.end_of_character()

    def end_of_word(self) -> None:
        """Handle end of word."""
        print("/", end=" ")
        self.timer.end_of_word()


class RpiTransmitter(Transmitter):
    """A Raspberry Pi transmitter."""

    def __init__(self, timer: ParisTimer):
        # import gpio here to avoid import errors on non-rpi platforms
        # pylint: disable=import-outside-toplevel
        import RPi.GPIO as GPIO  # Import the RPi.GPIO module
        self.GPIO = GPIO
        self.timer = timer
        self.GPIO.setmode(self.GPIO.BCM) 
        self.GPIO.setup(4, self.GPIO.OUT)
        self.GPIO.output(4, self.GPIO.LOW)

    def __del__(self):
        self.GPIO.output(4, self.GPIO.LOW)
        self.GPIO.cleanup()
        self.GPIO.cleanup()

    def transmit(self, dot_or_dash: int) -> None:
        self.GPIO.output(4, self.GPIO.HIGH)
        self.timer.dot_or_dash(dot_or_dash)
        self.GPIO.output(4, self.GPIO.LOW)
        self.GPIO.output(4, self.GPIO.LOW)

    def end_of_character(self) -> None:
        """Handle end of character."""
        self.timer.end_of_character()

    def end_of_word(self) -> None:
        """Handle end of word."""
        self.timer.end_of_word()
