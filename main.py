import sys

from tang import Controller
from signal import signal, SIGINT

def signal_handler(signal, frame):
    controller.close()
    sys.exit(0)

if __name__ == '__main__':
    controller = Controller(5730)
    signal(SIGINT, signal_handler)
    controller.start()
