import argparse
import waitress

from tutor_site import app
from tutor_site import config as cfg


def main(args: argparse.Namespace):
    debug = args.debug

    host = cfg.SERVER_HOST
    port = cfg.SERVER_PORT
    if debug:
        app.run(host=host, port=port, debug=debug)
    else:
        waitress.serve(app, host=host, port=port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--debug',
                        required=False,
                        action='store_true',
                        default=False,
                        help=('If it is not set, the application will use '
                              'waitress as a WSGI server. Otherwise, it will '
                              'be run on default Flask server in a debug '
                              'mode'))

    args = parser.parse_args()
    main(args)
