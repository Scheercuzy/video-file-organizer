import logging
import os
import argparse
import sys

# import rpyc
# from rpyc.utils.server import ThreadedServer
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler

from video_file_organizer.app import App

logger = logging.getLogger('vfo')


def parse_args(args):
    parser = argparse.ArgumentParser()
    # Config Parameters
    parser.add_argument('--config-file', action='store', nargs=1, type=str)
    parser.add_argument('--input-dir', action='store', nargs=1, type=str)
    parser.add_argument('--series-dirs', action='store', nargs='+', type=str)
    parser.add_argument('--ignore', action='store', nargs='+')
    parser.add_argument('--before-scripts', action='store',
                        nargs='+', type=str)
    parser.add_argument('--on-transfer-scripts',
                        action='store', nargs='+', type=str)
    parser.add_argument('--schedule', action='store', nargs=1, type=int)
    # RuleBook Parameters
    parser.add_argument('--rule-book-file', action='store', nargs=1, type=str)
    parser.add_argument('--series-rule', action='append', nargs='+', type=str,
                        metavar=('serie', 'rules'))
    # Logging Parameters
    parser.add_argument('-v', '--verbose', action='store_true')
    # ToolKit
    parser.add_argument('--create-config', action='store_true')
    parser.add_argument('--scheduler', action='store_true')
    parser.add_argument('--rpyc-host', action='store', default='localhost')
    parser.add_argument('--rpyc-port', action='store', default='2324',
                        type=int)
    return parser.parse_args(args)


def setup_logging(args):
    # Setup Logger
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('vfo.log')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # Set log level based on input arguments
    if os.environ.get('LOG') == "DEBUG" or args.verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    file_format = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s')
    console_format = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s')

    ch.setFormatter(console_format)
    fh.setFormatter(file_format)

    logger.addHandler(ch)
    logger.addHandler(fh)

    if os.environ.get('LOG') == "DEBUG" or args.verbose:
        logger.info("Running in verbose mode")


def toolkit(args):
    if args.create_config:
        from video_file_organizer.config import Config, RuleBook
        Config.create_file_from_template()
        RuleBook.create_file_from_template()
        sys.exit(0)

    if args.scheduler:
        from video_file_organizer import rpyc
        from video_file_organizer.scheduler import scheduler
        from video_file_organizer.config import Config
        # logging.basicConfig()
        # logging.getLogger('apscheduler').setLevel(logging.DEBUG)
        config = Config(args)

        scheduler.add_job(
            run_app,
            'interval',
            minutes=config.schedule,
            args={'args': args},
            name='vfo')
        logger.info(
            f"Scheduler Started! Running every {config.schedule} minute(s)")
        scheduler.start()

        try:
            logger.info("RPYC Server running")
            rpyc.server.start()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            scheduler.shutdown()

        sys.exit(0)


def main():
    setup_logging(args)
    toolkit(args)
    run_app(args)


def run_app(args=None, **kwargs):
    app = App()
    app.setup(args).run(**kwargs)


args = parse_args(sys.argv[1:])

if __name__ == "__main__":
    main()
