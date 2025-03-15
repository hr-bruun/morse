"""Module providing transmitter classes for morse code."""

from abc import ABC, abstractmethod

from .timer import ParisTimer


class Transmitter(ABC):
    """An abstract transmitter class."""

    @abstractmethod
    def transmit(self, dot_or_dash: int) -> None:
        """Transmit a dot or dash."""
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def end_of_word(self) -> None:
        """Handle end of word."""
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def end_of_character(self) -> None:
        """Handle end of character."""
        raise NotImplementedError("Subclasses must implement this method")


class DebugTransmitter(Transmitter):
    """A debug transmitter."""

    def __init__(self, timer: ParisTimer):
        self.timer = timer

    def __del__(self):
        self._output("\n")

    def transmit(self, dot_or_dash: int) -> None:
        """Transmit a dot or dash."""
        self._output("." if dot_or_dash == 0 else "-")
        self.timer.dot_or_dash(dot_or_dash)
        self.timer.end_of_dot_or_dash()

    def end_of_character(self) -> None:
        """Handle end of character."""
        self._output("/")
        self.timer.end_of_character()

    def end_of_word(self) -> None:
        """Handle end of word."""
        self._output("/")
        self.timer.end_of_word()

    def _output(self, symbol: str) -> None:
        """Output a symbol and flush."""
        print(symbol, end="", flush=True)


class RpiTransmitter(Transmitter):
    """A Raspberry Pi transmitter."""

    def __init__(self, timer: ParisTimer):
        # import gpio here to avoid import errors on non-rpi platforms
        # pylint: disable=import-outside-toplevel
        from RPi import GPIO
        self.gpio = GPIO
        self.timer = timer
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(4, self.gpio.OUT)
        self.gpio.output(4, self.gpio.LOW)

    def __del__(self):
        self.gpio.output(4, self.gpio.LOW)
        self.gpio.cleanup()
        self.gpio.cleanup()

    def transmit(self, dot_or_dash: int) -> None:
        self.gpio.output(4, self.gpio.HIGH)
        self.timer.dot_or_dash(dot_or_dash)
        self.gpio.output(4, self.gpio.LOW)
        self.gpio.output(4, self.gpio.LOW)

    def end_of_character(self) -> None:
        """Handle end of character."""
        self.timer.end_of_character()

    def end_of_word(self) -> None:
        """Handle end of word."""
        self.timer.end_of_word()
