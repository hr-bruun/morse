"""Module providing morse code functionality."""

import argparse
from abc import ABC, abstractmethod
import time
from typing import List

from .alphabet import ALPHABET
from .timer import Timer, ParisTimer
from .transmitters import Transmitter, DebugTransmitter, RpiTransmitter


class Morse:
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


def main():
    """
    Entry point for the Morse sender application.
    This function parses command-line arguments to determine the message to send,
    the speed of the message in words per minute, and whether to send the message
    to hardware or use a debug transmitter. It then sends the message using the
    specified parameters.
    """
    parser = argparse.ArgumentParser(description='Morse sender application')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', help='the message to send')
    group.add_argument('-f', '--file', type=argparse.FileType('r'),
                       help='a file with the message to send')
    parser.add_argument('--wpm', nargs='?', const=2, type=int, default=2,
                        help='the speed of the message in words per minute (default is 1)')
    parser.add_argument('--hw', action='store_true')

    args = parser.parse_args()

    message = "paris"
    if args.file:
        message = args.file.read().replace('\n', '')

    if args.m:
        message = args.m

    if args.hw:
        timer = ParisTimer(args.wpm)
        transmitter = RpiTransmitter(timer)
    else:
        timer = Timer()
        transmitter = DebugTransmitter(timer)
    morse = Morse(transmitter)

    print(f'Sending message: {message}')
    print(f'Words per minute: {args.wpm}')
    print(f'Dit speed in seconds: {timer.dit_length()}')
    print(f'Sending to hardware: {args.hw}')

    morse.send_message(message)


if __name__ == "__main__":
    main()
