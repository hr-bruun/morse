"""Module providing classes for timing and transmitting morse code."""

from abc import ABC, abstractmethod
import time

from .alphabet import ALPHABET

class Morse:  # pylint: disable=too-few-public-methods
    """Class represending a morse code sender"""

    def __init__(self, transmitter):
        self.transmitter = transmitter

    def send_message(self, message):  # pylint: disable=missing-function-docstring
        for letter in message.lower():
            self._send_letter(letter)
        self._send_letter(" ")

    def _send_letter(self, letter):
        if letter == " ":
            self.transmitter.end_of_word()
        else:
            for dot_or_dash in ALPHABET[letter]:
                self.transmitter.transmit(dot_or_dash)

            self.transmitter.end_of_character()


class ParisTimer:
    """A morse code timer using Paris timing."""

    INTER_WORD_PAUSE = 7

    def __init__(self, wpm):  # [missing-function-docstring]
        self.dit_length = ParisTimer.calculate_dit_length(wpm)

    def end_of_word(self):  # [missing-function-docstring]
        self._pause(self.INTER_WORD_PAUSE)

    def end_of_character(self):  # [missing-function-docstring]
        self._pause(2) # Makes 3 in all for inter-character space

    def end_of_dot_or_dash(self):  # [missing-function-docstring]
        self._pause(1) # intra-character space

    def dot_or_dash(self, dot_or_dash):  # [missing-function-docstring]
        self._pause(1 if dot_or_dash == 0 else 3)

    def _pause(self, units):  # [missing-function-docstring]
        time.sleep(units * self.dit_length)

    @staticmethod
    def calculate_dit_length(wpm):  # [missing-function-docstring]
        # Using the "PARIS" standard word (50 units long)
        return 60 / (50 * wpm)


class Transmitter(ABC):
    """An abstract transmitter class."""


    @abstractmethod
    def transmit(self, signal: int) -> None:
        pass

    @abstractmethod
    def end_of_character(self) -> None:
        pass

    @abstractmethod
    def end_of_word(self) -> None:
        pass


class DebugTransmitter(Transmitter):
    """A debug transmitter."""

    def __init__(self, timer):  # [missing-function-docstring]
        self.timer = timer

    def transmit(self, signal: int) -> None:  # [missing-function-docstring]
        if signal == 0:
            self._debug("dot")
        else:
            self._debug("dash")
        self.timer.dot_or_dash(signal)
        self.timer.end_of_dot_or_dash()

    def end_of_character(self) -> None:  # [missing-function-docstring]
        self._debug("/") # end of character /
        self.timer.end_of_character()

    def end_of_word(self) -> None:  # [missing-function-docstring]
        self._debug("/") # extra / to finish word
        print(" - inter word pause - ")
        self.timer.end_of_word()

    def _debug(self, msg):  # [missing-function-docstring]
        print(msg, end=' ', flush=True)


class RpiTransmitter(Transmitter):
    """A Raspberry Pi transmitter."""

    GPIO_PIN = 4

    def __init__(self, timer):  # [missing-function-docstring]
        from RPi import GPIO
        self.timer = timer

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_PIN, GPIO.OUT)
        GPIO.output(self.GPIO_PIN, GPIO.LOW)

    def cleanup_gpio(self):  # [missing-function-docstring]
        GPIO.output(self.GPIO_PIN, GPIO.LOW)
        GPIO.cleanup()

    def transmit(self, signal: int) -> None:  # [missing-function-docstring]
        GPIO.output(GPIO_PIN, GPIO.HIGH)
        self.timer.dot_or_dash(signal)
        GPIO.output(GPIO_PIN, GPIO.LOW)
        self.timer.end_of_dot_or_dash()

    def end_of_character(self) -> None:  # [missing-function-docstring]
        self.timer.end_of_character()

    def end_of_word(self) -> None:  # [missing-function-docstring]
        self.timer.end_of_word()
