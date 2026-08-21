"""The only module that knows where the store lives or what format it is in.

See docs/architecture/adr/ADR-0002-one-store-file-per-user.md.
"""

import json
import os
import tempfile
from pathlib import Path

from expenses.errors import ExpensesError

VERSION = 1


def store_path():
    """The single store file for this user.

    ``EXPENSES_STORE`` wins when it is set and non-empty. It exists so tests can
    exercise a real store without touching the developer's own; it is not a way
    to keep several friend groups apart (ADR-0002 decision 2).
    """
    override = os.environ.get("EXPENSES_STORE")
    if override:
        return Path(override)
    data_home = os.environ.get("XDG_DATA_HOME")
    if data_home:
        return Path(data_home) / "expenses" / "store.json"
    return Path.home() / ".local" / "share" / "expenses" / "store.json"


def empty():
    return {"version": VERSION, "people": [], "expenses": []}


def load():
    """The store's contents, or an empty group when the file does not exist.

    A file that exists but cannot be read or understood is fatal and is left
    exactly as it is (ADR-0002 decision 6). Nothing here repairs, ignores or
    truncates anything.
    """
    path = store_path()
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return empty()
    except OSError as exc:
        raise ExpensesError("cannot read {}: {}".format(path, exc.strerror or exc))
    except ValueError as exc:  # undecodable bytes
        raise ExpensesError("cannot read {}: it is not valid UTF-8 text ({})".format(path, exc))

    try:
        data = json.loads(text)
    except ValueError as exc:
        raise ExpensesError(
            "cannot read {}: it is not valid JSON ({}). "
            "Nothing has been changed; fix or move the file and try again.".format(path, exc)
        )

    if not isinstance(data, dict) or not isinstance(data.get("people"), list) \
            or not isinstance(data.get("expenses"), list):
        raise ExpensesError(
            "cannot read {}: it is not an expenses store. "
            "Nothing has been changed; fix or move the file and try again.".format(path)
        )
    # The containers being lists is not enough. Everything above this module
    # treats a roster entry as a string, so a `people` list holding anything
    # else parses here and then breaks somewhere that has no idea it is looking
    # at a damaged file -- which is a traceback, not the named error ADR-0002
    # decision 6 requires (WI-0001 AC8, review.md F1).
    for entry in data["people"]:
        if not isinstance(entry, str):
            raise ExpensesError(
                "cannot read {}: its list of people contains {}, which is not a name. "
                "Nothing has been changed; fix or move the file and try again.".format(
                    path, type(entry).__name__
                )
            )
    return data


def save(data):
    """Replace the store atomically.

    The temporary file is created in the store's own directory, because
    ``os.replace`` is only atomic within one filesystem -- writing it to /tmp
    would turn this into a copy and reintroduce the half-written file ADR-0002
    decision 7 exists to prevent.
    """
    path = store_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=".store-", suffix=".tmp")
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as tmp:
                json.dump(data, tmp, ensure_ascii=False, indent=2, sort_keys=True)
                tmp.write("\n")
            os.replace(tmp_name, str(path))
        except BaseException:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise
    except OSError as exc:
        raise ExpensesError("cannot write {}: {}".format(path, exc.strerror or exc))
