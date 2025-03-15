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
        from RPi import GPIO  # type: ignore
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
