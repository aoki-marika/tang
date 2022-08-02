import sys
import argparse

from tang import Controller
from signal import signal, SIGINT

def main():
    parser = argparse.ArgumentParser(description='Host a mock Spice API server.')

    server_group = parser.add_argument_group('server')
    server_group.add_argument('--port', dest='port', help='port to host on', type=int, default=5730)
    server_group.add_argument('--password', dest='password', help='encryption password', type=str)

    args = parser.parse_args()

    controller = Controller(args.port, password=args.password)

    def signal_handler(signal, frame):
        controller.close()
        sys.exit(0)

    signal(SIGINT, signal_handler)
    controller.start()

if __name__ == '__main__':
    main()
