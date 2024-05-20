from argparse import ArgumentParser

import ardsmm
import os.path
import platform
import json
import sys

PROG_NAME = os.path.basename(os.path.dirname(__file__))
IS_WINDOWS = platform.platform().startswith("Windows")
INPUT_CONT_MSG = "CTRL-D"
if IS_WINDOWS:
    INPUT_CONT_MSG = "enter"


def parse_args():
    parser = ArgumentParser(prog=PROG_NAME)
    parser.add_argument("-i", "--in-place", action="store_true", help="modify JSON config file in-place")
    parser.add_argument("-o", "--output-file", type=str, help="write JSON output to file (default: stdout)")
    parser.add_argument("-m", "--mod-file", type=str, help="read mods from file (default: stdin)")
    parser.add_argument("-I", "--indent", type=int, default=4, help=f"set JSON indentation level (default: {ardsmm.ArmaConfig.DEFAULT_INDENT})")
    parser.add_argument("-V", "--version", action="store_true", help="display version number and exit")
    parser.add_argument("configfile", type=str, nargs="?", help="An Arma Reforger dedicated server JSON config")
    return parser.parse_args()


def main():
    args = parse_args()
    input_data = ""

    if args.version:
        print(ardsmm._version.__version__)
        return 0

    if not args.configfile:
        print("Missing required positional argument: configfile", file=sys.stderr)
        return 1

    if args.in_place and args.output_file:
        print("-i/--in-place and -o/--output-file are mutually exclusive options", file=sys.stderr)
        return 1

    if args.mod_file:
        print(f"Reading Arma Reforger mod list from {args.mod_file}", file=sys.stderr)
        if os.path.exists(args.mod_file):
            input_data = open(args.mod_file).read()
        else:
            print(f"Input file not found: {args.mod_file}", file=sys.stderr)
            return 1
    else:
        if sys.stdin.isatty():
            print(f"\nPaste Arma Reforger mod list and hit {INPUT_CONT_MSG} to continue...\n",
                  file=sys.stderr)

        if IS_WINDOWS:
            while True:
                line = sys.stdin.readline()
                if not line.rstrip():
                    break
                input_data += line
        else:
            input_data = sys.stdin.read()

    if not input_data:
        print("Warning: No mods consumed!", file=sys.stderr)

    config = ardsmm.ArmaConfig(args.configfile)
    try:
        data = json.loads("[" + input_data + "]")
        for x in data:
            config.append_mod(x)
        config.update()
    except json.JSONDecodeError as e:
        print("Invalid JSON", file=sys.stderr)
        print(f"Reason: {e}", file=sys.stderr)
        return 1

    filename = ""
    if args.output_file:
        filename = args.output_file
    elif args.in_place:
        filename = args.configfile

    if filename:
        print(f"Writing to {filename}", file=sys.stderr)
        with open(filename, "w+") as fp:
            fp.write(config.to_string(args.indent))
    else:
        print(config.to_string(args.indent))

    return 0


if __name__ == "__main__":
    sys.exit(main())
