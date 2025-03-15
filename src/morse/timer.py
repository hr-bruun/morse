"""Module providing timing functionality for morse code."""

import time

class Timer:
    """Base class for morse code timers."""

    def end_of_word(self) -> None:
        """Pause at the end of a word."""

    def end_of_character(self) -> None:
        """Pause at the end of a character."""

    def end_of_dot_or_dash(self) -> None:
        """Pause at the end of a dot or dash."""

    def dot_or_dash(self, dot_or_dash: int) -> None:
        """Transmit a dot or dash."""

    def dit_length(self) -> float:
        """Return the length of a dit."""
        return 0


class ParisTimer(Timer):
    """A morse code timer using Paris timing."""

    INTER_WORD_PAUSE = 7

    def __init__(self, wpm: int):
        self.wpm = wpm

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

    def dit_length(self) -> float:
        """Calculate the length of a dit based on words per minute."""
        # Using the "PARIS" standard word (50 units long)
        return 60 / (50 * self.wpm)
