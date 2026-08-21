"""The only layer that parses arguments, prints, or chooses an exit status."""

import argparse
import sys

from expenses import people, store
from expenses.errors import ExpensesError

FAILURE = 2


def build_parser():
    parser = argparse.ArgumentParser(
        prog="python3 -m expenses",
        description="Track shared expenses in a friend group.",
    )
    sub = parser.add_subparsers(dest="command")

    add_person = sub.add_parser("add-person", help="add a person to the group")
    add_person.add_argument("name", help="the name they are known by")

    sub.add_parser("people", help="list the people in the group")
    return parser


def cmd_add_person(args, out):
    # Load before anything is written: a damaged store must abort before a
    # write, not after one (AC6, ADR-0002 decision 6).
    data = store.load()
    added = people.add(data, args.name)
    store.save(data)
    print("Added {}.".format(added), file=out)
    return 0


def cmd_people(args, out):
    data = store.load()
    names = people.listing(data)
    if not names:
        print("Nobody in the group yet.", file=out)
        return 0
    for name in names:
        print(name, file=out)
    return 0


COMMANDS = {"add-person": cmd_add_person, "people": cmd_people}


def main(argv=None, out=None, err=None):
    out = sys.stdout if out is None else out
    err = sys.stderr if err is None else err
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help(err)
        return FAILURE
    try:
        return COMMANDS[args.command](args, out)
    except ExpensesError as exc:
        # The expected failures: a message written for the person at the
        # terminal, already saying what was wrong.
        print(str(exc), file=err)
        return FAILURE
    except Exception as exc:  # noqa: BLE001 -- deliberate, see below
        # The backstop, and the reason AC8 is a property of this function
        # rather than of every module below it agreeing to raise only
        # ExpensesError. Without it, AC8 is true only for the failure modes
        # someone has already thought of -- which is exactly how a damaged
        # store reached the user as an AttributeError traceback (review.md F1).
        #
        # It reports rather than swallows: the type and message are on the
        # line, so the failure is still diagnosable, and it says plainly that
        # this one is the tool's fault and not the user's. BaseException is not
        # caught, so KeyboardInterrupt and SystemExit behave as they should.
        # Deliberately does not claim "nothing was written": an unexpected
        # failure can land after store.save(), and a reassurance this function
        # cannot verify is worse than none.
        print(
            "an internal error in expenses ({}: {}). This is a bug in the tool, "
            "not something you did wrong.".format(type(exc).__name__, exc),
            file=err,
        )
        return FAILURE
