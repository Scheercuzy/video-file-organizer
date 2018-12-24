import argparse
import logging

from video_file_organizer.app import App


def main():
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="Displays debug messages",
                        action="store_true")
    parser.add_argument("-c", "--config",
                        help="Custom config files location",
                        nargs=1)
    args = parser.parse_args()

    # Setup Logger
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('vfo.log')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # Set log level based on input arguments
    if args.verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    file_format = logging.Formatter(
        '%(asctime)s - %(levelname)s:%(message)s')
    console_format = logging.Formatter(
        '%(message)s')

    ch.setFormatter(console_format)
    fh.setFormatter(file_format)

    logger.addHandler(ch)
    logger.addHandler(fh)

    if args.config:
        app = App(args.config[0], args)
    else:
        app = App(args)
    app.setup()
    app.run()


if __name__ == "__main__":
    main()
