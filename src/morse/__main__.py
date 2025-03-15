"""
This module serves as the entry point for the Morse code project.

It imports the main function from the morse module and executes it
when the script is run as the main module.

Usage:
    python -m morse

Functions:
    main: The main function that runs the Morse code application.
"""

from .morse import main

if __name__ == "__main__":
    main()
