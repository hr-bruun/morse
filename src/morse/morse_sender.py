'''
A program that can send a morse message to a connected LED.

The LED is expected to be connected to GPIO 4 (BCM naming)

The message to send is specified with the -m parameter

    '''

import argparse

from .morse import Morse, DebugTransmitter, ParisTimer, RpiTransmitter


def main():  # pylint: disable=missing-function-docstring
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

    timer = ParisTimer(args.wpm)
    if args.hw:
        transmitter = RpiTransmitter(timer)
    else:
        transmitter = DebugTransmitter(timer)
    morse = Morse(transmitter)

    print(f'Sending message: {message}')
    print(f'Words per minute: {args.wpm}')
    print(f'Dit speed in seconds: {timer.dit_length}')
    print(f'Sending to hardware: {args.hw}')

    morse.send_message(message)

if __name__ == "__main__":
    main()
