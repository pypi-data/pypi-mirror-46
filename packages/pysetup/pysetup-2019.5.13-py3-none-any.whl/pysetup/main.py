from .command import Command
import sys


def main():
    return Command.exec(*sys.argv[1:])
