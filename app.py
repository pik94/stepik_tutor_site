import argparse

from tutor_site import app


def main(args: argparse.Namespace):
    debug = args.debug
    if debug not in [0, 1]:
        raise ValueError((f'Unknown a debug mode. A value should be 0 or 1, '
                          f'but {debug} was given.'))

    debug = bool(debug)

    host = args.host
    port = args.port
    app.run(host=host, port=port, debug=debug)


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

    parser.add_argument('-ho',
                        '--host',
                        required=False,
                        type=str,
                        default='localhost',
                        help='Set a host of the server.')

    parser.add_argument('-p',
                        '--port',
                        required=False,
                        type=int,
                        default=8080,
                        help='Set a port of the server.')

    args = parser.parse_args()
    main(args)
