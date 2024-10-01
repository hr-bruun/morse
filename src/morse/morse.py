from abc import ABC, abstractmethod
import time
from typing import List

from .alphabet import ALPHABET

class Morse:
    
    def __init__(self, transmitter):
        self.transmitter = transmitter

    def send_message(self, message):
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
    INTER_WORD_PAUSE = 7

    def __init__(self, wpm):
        self.dit_length = ParisTimer.dit_length(wpm)

    def end_of_word(self):
        self._pause(self.INTER_WORD_PAUSE) 

    def end_of_character(self):
        self._pause(2) # Makes 3 in all for inter-character space

    def end_of_dot_or_dash(self):
        self._pause(1) # intra-character space

    def dot_or_dash(self, dot_or_dash):
        self._pause(1 if dot_or_dash == 0 else 3)

    def _pause(self, units):
        time.sleep(units * self.dit_length)

    @staticmethod
    def dit_length(wpm):
        # Using the "PARIS" standard word (50 units long) 
        return 60 / (50 * wpm)


class Transmitter(ABC):
    
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
    def __init__(self, timer):
        self.timer = timer

    def transmit(self, signal: int) -> None:
        if signal == 0:
            self._debug("dot")
        else:
            self._debug("dash")
        self.timer.dot_or_dash(signal)
        self.timer.end_of_dot_or_dash()

    def end_of_character(self) -> None:
        self._debug("/") # end of character /
        self.timer.end_of_character()

    def end_of_word(self) -> None:
        self._debug("/") # extra / to finish word
        print(" - inter word pause - ")
        self.timer.end_of_word()

    def _debug(self, msg):
        print(msg, end=' ', flush=True)


class RpiTransmitter(Transmitter):
    GPIO_PIN = 4
    
    def __init__(self, timer):
        import RPi.GPIO as GPIO
        self.timer = timer

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_PIN, GPIO.OUT)
        GPIO.output(self.GPIO_PIN, GPIO.LOW)

    def cleanup_gpio(self):
        GPIO.output(self.GPIO_PIN, GPIO.LOW)
        GPIO.cleanup()

    def transmit(self, signal: int) -> None:
        GPIO.output(GPIO_PIN, GPIO.HIGH)
        self.timer.dot_or_dash(signal)
        GPIO.output(GPIO_PIN, GPIO.LOW)
        self.timer.end_of_dot_or_dash()

    def end_of_character(self) -> None:
        self.timer.end_of_character()

    def end_of_word(self) -> None:
        self.timer.end_of_word()
