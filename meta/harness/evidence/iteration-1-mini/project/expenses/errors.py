class ExpensesError(Exception):
    """A failure with a message written for the person at the terminal.

    Every failure below the CLI layer is *meant* to be one of these. ``cli.main``
    catches it once, prints ``str(exc)`` on stderr and exits non-zero.

    That alone does not make WI-0001 AC8 -- no traceback ever reaches the user
    -- true, and this docstring used to claim it did. It makes AC8 true for
    every failure somebody remembered to raise as an ``ExpensesError``; the one
    nobody remembered still escaped as a traceback, which is exactly what
    happened with a damaged store (``review.md`` F1). AC8 is a property of
    ``cli.main`` having a *second*, catch-all handler behind this one. This
    class is what makes the common path say something useful; the backstop is
    what makes the guarantee unconditional.
    """
