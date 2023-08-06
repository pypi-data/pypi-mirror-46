import os
import sys
import argparse
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

__version__ = "0.1.0"

def _load_config(file_path):
    if not os.path.exists(file_path):
        sys.exit(2)

    c = configparser.ConfigParser()
    c.read('example.cfg')
    return c


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stdout.write('Error: {}'.format(message))
        self.print_help()
        sys.exit(2)


def _cli_options():
    parser = MyParser(description="Commandline tool to download Defold's Bob")
    parser.add_argument('get', help="get a value in a edit-editconfig")
    parser.add_argument('set', help="set a value in a edit-editconfig")
    parser.add_argument('-f', '--file', dest='file', help="the file")
    parser.add_argument('-s', '--section', dest='section', help="the section")
    parser.add_argument('-k', '--key', dest='key', help="the key")
    parser.add_argument('-v', '--value', dest='value', help="the value")

    return parser


def _run_cli():
    parser = _cli_options()
    options = parser.parse_args()
    c = _load_config(options.file)
    if options.command == "get":
        print(c.get(options.section, options.key))
    elif options.command == "set":
        print(c.set(options.section, options.key, options.set))
        with open(options.file, 'wb') as configfile:
            c.write(configfile)


def main():
    try:
        _run_cli()
    except KeyboardInterrupt:
        sys.exit()
    except:
        raise