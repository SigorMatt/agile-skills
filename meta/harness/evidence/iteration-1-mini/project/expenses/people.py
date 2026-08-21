"""Roster rules. Pure: no I/O, no printing, no exit codes.

WI-0001 AC3 and AC7, and ADR-0006 rules 4-6.
"""

from expenses.errors import ExpensesError


def normalise(name):
    """The stored spelling of a name, or an error saying why it is not one.

    Surrounding whitespace is stripped (AC3). Empty and whitespace-only names
    are rejected (AC7). Control characters are rejected for one specific reason
    and not as general hygiene: AC1 requires the listing to print one name per
    line, so a newline in a name produces a listing that cannot be read back,
    and an escape sequence can overwrite what a terminal has already drawn
    (ADR-0006 rule 5). Everything else printable -- commas, spaces, digits,
    punctuation, non-ASCII -- is allowed, because no argument value in this tool
    is ever split on a delimiter (ADR-0006 rule 3).
    """
    if name is None:
        raise ExpensesError("a name is required")
    stripped = name.strip()
    if not stripped:
        raise ExpensesError("a name is required")
    for char in stripped:
        if ord(char) < 0x20 or ord(char) == 0x7F:
            raise ExpensesError(
                "a name cannot contain control characters (found {!r})".format(char)
            )
    return stripped


def match_key(name):
    """The key two names are compared by: stripped, then lowercased.

    ``str.lower`` is not full Unicode case-folding; ADR-0006 records that as
    accepted for a friend group. It is the **single** place that rule is
    written: ``add`` compares through this function on both sides rather than
    lowercasing inline, so changing the rule here changes it everywhere, and
    WI-0002 can match a sharer against the roster by the same key.

    It compares; it does not validate. That separation is deliberate. It used
    to call ``normalise``, which meant every name already in the store was
    re-validated on every add, and a stored name that today's rules reject made
    the name being *typed* look wrong -- ``add-person Carol`` reporting a
    control character Carol does not contain (review.md F2). Validation belongs
    at the point a name enters the roster, which is ``normalise`` on the input
    side, and it happens exactly once. A caller matching user input against the
    roster should call ``normalise`` on that input first, as ``add`` does.
    """
    return name.strip().lower()


def add(data, name):
    """Add one person, or raise naming the person already there."""
    stripped = normalise(name)
    key = match_key(stripped)
    for existing in data["people"]:
        if match_key(existing) == key:
            raise ExpensesError(
                "{} is already in the group; nothing was added".format(existing)
            )
    data["people"].append(stripped)
    return stripped


def listing(data):
    """The stored spellings, in the order they were added."""
    return list(data["people"])
