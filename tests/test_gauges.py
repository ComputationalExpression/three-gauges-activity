"""Automated checks for Activity 6: Three Gauges.

The function checks call each of your functions directly, the way main does,
and look at the value it returns. A function that prints its answer instead of
returning it hands back None, and the functions themselves print nothing.

The program check runs main() in a scratch folder holding its own
data/meadville.csv, data/saegertown.csv and data/cussewago.csv, and reads the
report lines. They are matched
loosely: any amount of whitespace, any letter case, and the colon is
optional, so `print("Highest:", x)`, `print("Highest: " + str(x))` and
`print(f"Highest: {x}")` all read the same.

When a check fails, the assertion message says what was called or which line
came out wrong, what came back, and what was expected.
"""

import re
from unittest.mock import patch

import pytest

import main

GAUGES = ["meadville", "saegertown", "cussewago"]


def function(name):
    """Return the student's function called `name`, or fail saying it is missing."""
    found = getattr(main, name, None)
    if not callable(found):
        pytest.fail(f"found no function called {name} in src/main.py: check the def line and its spelling")
    return found


def expect_return(capsys, name, args, want):
    """Call the function `name` with `args` and check what it returns and prints."""
    got = function(name)(*args)
    shown = ", ".join(repr(arg) for arg in args)
    printed = capsys.readouterr().out.strip()
    if got is None:
        raise AssertionError(f"{name}({shown}) returned None: end the function with return, not print")
    assert got == want, f"{name}({shown}) returned {got!r}, expected {want!r}"
    assert printed == "", (
        f"{name}({shown}) printed {printed!r}: return the answer and let main print it"
    )


def values(out, label):
    """Return every value printed after `label`, normalized, in order."""
    words = r"\s+".join(re.escape(word) for word in label.split())
    found = re.findall(rf"^\s*{words}\s*:?\s*([^\n]*)", out, re.IGNORECASE | re.MULTILINE)
    return [" ".join(value.split()).upper().rstrip(".! ") for value in found]


def expected_report(readings, watch):
    """The three numbers a report gives for one gauge."""
    return (
        max(readings),
        len([reading for reading in readings if reading >= watch]),
        sum(readings) // len(readings),
    )


def write_gauge(path, readings):
    """Write one gauge's CSV file: a header line, then one date and level per line."""
    lines = ["date,level"] + [f"2026-06-{day:02d},{level}" for day, level in enumerate(readings, 1)]
    path.write_text("\n".join(lines) + "\n")


def run(capsys, monkeypatch, tmp_path, watch, lists):
    """Run main() once in a scratch folder whose data/ files hold `lists`."""
    (tmp_path / "data").mkdir()
    for gauge, readings in zip(GAUGES, lists):
        write_gauge(tmp_path / "data" / f"{gauge}.csv", readings)
    monkeypatch.chdir(tmp_path)
    with patch("builtins.input", side_effect=["JJ", str(watch)]):
        main.main()
    out, err = capsys.readouterr()
    assert err == "", "the program wrote to the error stream:\n" + err
    return out


def test_program_prints_the_same_report(capsys, monkeypatch, tmp_path):
    for case, (watch, lists) in enumerate([
        (40, [[31, 34, 52, 68, 45, 39, 36], [28, 30, 41, 57, 49, 35, 33], [12, 15, 22, 26, 19, 17, 14]]),
        (20, [[5, 9, 3], [40, 20, 10, 30], [21, 22]]),
    ]):
        folder = tmp_path / f"run{case}"
        folder.mkdir()
        out = run(capsys, monkeypatch, folder, watch, lists)
        context = f"watch={watch}, readings in the data files: {lists}"
        want = [expected_report(readings, watch) for readings in lists]
        for position, label in enumerate(["Highest", "Reached watch", "Average"]):
            expected = [str(report[position]) for report in want]
            got = values(out, label)
            assert got == expected, (
                f'the "{label}" lines said {got}, expected {expected}, one per gauge '
                f"in the order Meadville, Saegertown, Cussewago ({context})"
            )
        peak = [str(max(max(readings) for readings in lists))]
        assert values(out, "Peak") == peak, (
            f'the "Peak" line said {values(out, "Peak")}, expected {peak} ({context})'
        )


def test_read_readings_returns_the_levels(capsys, tmp_path):
    for readings in ([12, 20, 7], [40, 41, 42, 43, 44]):
        path = tmp_path / f"gauge{len(readings)}.csv"
        write_gauge(path, readings)
        got = function("read_readings")(str(path))
        printed = capsys.readouterr().out.strip()
        call = f'read_readings("{path.name}") on a file of {len(readings)} levels'
        if got is None:
            raise AssertionError(f"{call} returned None: end the function with return, not print")
        assert got == readings, (
            f"{call} returned {got!r}, expected {readings!r}: skip the header line, "
            "and convert each level with int"
        )
        assert printed == "", f"{call} printed {printed!r}: return the list and let main print"


def test_highest_returns_the_largest(capsys):
    # Largest in the middle, at the end, and at the very start.
    expect_return(capsys, "highest", ([12, 20, 7],), 20)
    expect_return(capsys, "highest", ([12, 20, 41],), 41)
    expect_return(capsys, "highest", ([55, 20, 41],), 55)


def test_count_at_or_above_returns_the_count(capsys):
    expect_return(capsys, "count_at_or_above", ([10, 20, 30], 20), 2)
    # A reading exactly at the level counts.
    expect_return(capsys, "count_at_or_above", ([10, 20, 30], 30), 1)
    expect_return(capsys, "count_at_or_above", ([10, 20, 30], 10), 3)
    # Zero is a number, not None: start the count at 0 and return it.
    expect_return(capsys, "count_at_or_above", ([10, 20, 30], 31), 0)


def test_average_returns_a_whole_number(capsys):
    # 305 // 7 is 43, where 305 / 7 would be 43.571...
    expect_return(capsys, "average", ([31, 34, 52, 68, 45, 39, 36],), 43)
    expect_return(capsys, "average", ([12, 20, 7],), 13)
