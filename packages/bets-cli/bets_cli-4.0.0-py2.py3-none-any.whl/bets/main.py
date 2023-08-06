#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import logging

from bets import __version__
from bets.model.scenario import ScenariosGenerator
from bets.program_io.matches_input import MatchesInput
from bets.program_io.matches_output import MatchesOutput
from bets.program_io.scenarios_output import ScenariosOutput

__author__ = "nachereshata"
__copyright__ = "nachereshata"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Bets CLI to assist football betting")

    parser.add_argument("-a", "--action",
                        dest="action",
                        help="[ matches | scenarios ]",
                        choices=["matches", "scenarios"],
                        metavar="ACTION",
                        default="matches")

    parser.add_argument("--in-file",
                        dest="in_file",
                        help="Path to the matches file. Defaults to 'matches.txt'.",
                        metavar="IN_FILE",
                        default="matches.txt")

    parser.add_argument("--in-fmt",
                        dest="in_fmt",
                        help="The format of the input file [ efbet | lines ]. Defaults to 'lines'.",
                        choices=["lines", "efbet"],
                        metavar="IN_FMT",
                        default="lines")

    parser.add_argument("--out-dest",
                        dest="out_dest",
                        help="Name of output destination. Can be set to a file, or defaults to 'console'",
                        metavar="OUT_DEST",
                        default="console")

    parser.add_argument("--out-fmt",
                        dest="out_fmt",
                        help="The output format of the results when printed to console. [ plain | fancy_grid | csv ]",
                        choices=["plain", "fancy_grid", "csv"],
                        metavar="OUT_FMT",
                        default="plain")

    parser.add_argument("--version",
                        action="version",
                        version="bets-cli {ver}".format(ver=__version__))

    parser.add_argument("-v", "--verbose",
                        dest="loglevel",
                        help="set loglevel to INFO",
                        action="store_const",
                        const=logging.INFO)

    parser.add_argument("-vv", "--very-verbose",
                        dest="loglevel",
                        help="set loglevel to DEBUG",
                        action="store_const",
                        const=logging.DEBUG)

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def _action_matches(in_file, in_fmt, out_dest, out_fmt):
    print("reading matches from ({})[{}]...".format(in_fmt, in_file))
    matches = MatchesInput.read_file(in_file, in_fmt)

    if out_dest != "console":
        print("got [{}] matches:".format(len(matches)))
        MatchesOutput.write_matches(matches, "console", "plain")

    print("writing [{}] matches ({}) to [{}]...\n".format(len(matches), out_fmt, out_dest))
    MatchesOutput.write_matches(matches, out_dest, out_fmt)
    print("Done writing matches!")


def _action_scenarios(in_file, in_fmt, out_dest, out_fmt):
    print("reading matches from ({})[{}]...".format(in_fmt, in_file))
    matches = MatchesInput.read_file(in_file, in_fmt)

    print("got [{}] matches:".format(len(matches)))
    MatchesOutput.write_matches(matches, "console", "plain")

    print("generating scenarios...")
    scenarios = list(ScenariosGenerator(matches).generate_scenarios())
    print("got total of [{}] scenarios".format(len(scenarios)))

    print("writing scenarios to ({})[{}]...".format(out_fmt, out_dest))
    ScenariosOutput.write_scenarios(scenarios, out_dest, out_fmt)
    print("Done writing scenarios to ({})[{}]...".format(out_fmt, out_dest))


ACTIONS = {
    "matches": _action_matches,
    "scenarios": _action_scenarios
}


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)

    print("Starting action [ {} ]...".format(args.action))
    ACTIONS[args.action](in_file=args.in_file, in_fmt=args.in_fmt, out_dest=args.out_dest, out_fmt=args.out_fmt)
    print("All Done!")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
