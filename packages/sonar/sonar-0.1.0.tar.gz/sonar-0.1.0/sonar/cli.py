import os
import sys
import argparse
import configparser
import datetime
from sonar.snap import main as snap_main
from sonar.map import main as map_main

# The following hack will allow snap and map to run without flask being installed
try:
    from sonar.web import main as web_main
except ModuleNotFoundError:

    def web_main(*args, **kwargs):
        print("Could not load Flask", file=sys.stderr)


def make_list(s):
    return s.split(",")


def today():
    d = datetime.datetime.now()
    return datetime.datetime.strftime(d, "%Y-%m-%d")


def main():

    # Inspired by https://stackoverflow.com/q/3609852
    parser = argparse.ArgumentParser(
        prog="sonar",
        description="Tool to profile usage of HPC resources by regularly probing processes using ps.",
        epilog="Run sonar <subcommand> -h to get more information about subcommands.",
    )

    subparsers = parser.add_subparsers(title="Subcommands", metavar="", dest="command")

    # parser for "snap"
    parser_snap = subparsers.add_parser(
        "snap",
        help="Take a snapshot of the system. Run this on every node and often (e.g. every 20 minutes).",
    )
    parser_snap.add_argument(
        "--cpu-cutoff",
        metavar="FLOAT",
        type=float,
        default=0.5,
        help="CPU Memory consumption percentage cutoff [default: %(default)s].",
    )
    parser_snap.add_argument(
        "--mem-cutoff",
        metavar="FLOAT",
        type=float,
        default=0.0,
        help="Memory consumption percentage cutoff [default: %(default)s].",
    )
    parser_snap.add_argument(
        "--ignored-users",
        metavar="STR,STR",
        default="",
        type=make_list,
        help="Users to ignore as comma-separated list [default: None].",
    )
    parser_snap.add_argument(
        "--output-delimiter",
        metavar="STR",
        default="\t",
        help=r"Delimiter for output columns [default: %(default)s].",
    )
    parser_snap.set_defaults(func=snap_main)

    # parser for "map"
    parser_map = subparsers.add_parser(
        "map",
        help="Parse the system snapshots and map applications. Run this only once centrally and typically once a day.",
    )
    parser_map.add_argument(
        "--input-dir",
        metavar="DIR",
        required=True,
        help="Path to the directory with the results of sonar snap (required).",
    )
    parser_map.add_argument(
        "--str-map-file",
        metavar="FILE",
        help="File with the string mapping information (process -> application).",
    )
    parser_map.add_argument(
        "--re-map-file",
        metavar="FILE",
        help="File with the regular expression mapping information (process -> application).",
    )
    parser_map.add_argument(
        "--default-category",
        metavar="STR",
        default="unknown",
        help="Default category for programs that are not recognized [default: %(default)s].",
    )
    parser_map.add_argument(
        "--input-suffix",
        metavar="STR",
        default=".tsv",
        help="Input file suffix [default: %(default)s].",
    )
    parser_map.add_argument(
        "--input-delimiter",
        metavar="STR",
        default="\t",
        help=r"Delimiter for input columns [default: %(default)s].",
    )
    parser_map.add_argument(
        "--output-delimiter",
        metavar="STR",
        default="\t",
        help=r"Delimiter for output columns [default: %(default)s].",
    )
    parser_map.set_defaults(func=map_main)

    # parser for the web frontend
    parser_map = subparsers.add_parser(
        "web",
        help="Run the web frontend to visualize results. This can run locally or on a server (via uWSGI).",
    )
    parser_map.add_argument("--debug", dest="debug", action="store_true", default=False)
    parser_map.add_argument(
        "--host", dest="host", default=os.environ.get("HOST", "127.0.0.1")
    )
    parser_map.add_argument(
        "--port", dest="port", type=int, default=int(os.environ.get("PORT", 5000))
    )
    parser_map.set_defaults(func=web_main)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit()

    try:
        # vars() converts object into a dictionary
        args = vars(args)
    except AttributeError:
        parser.print_help()

    args["func"](args)
