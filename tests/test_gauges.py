"""Automated checks for Activity 6: Three Gauges.

The function checks call each of your functions directly, the way main does,
and look at the value it returns. A function that prints its answer instead of
returning it hands back None.

The program check runs main() and reads the report lines. They are matched
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


def expect_return(name, args, want):
    """Call the function `name` with `args` and check what it returns."""
    got = function(name)(*args)
    shown = ", ".join(repr(arg) for arg in args)
    if got is None:
        raise AssertionError(f"{name}({shown}) returned None: end the function with return, not print")
    assert got == want, f"{name}({shown}) returned {got!r}, expected {want!r}"


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


def run(capsys, watch, lists=None):
    """Run main() once, optionally with different readings for each gauge."""
    original = {gauge: getattr(main, gauge) for gauge in GAUGES}
    if lists is not None:
        for gauge, readings in zip(GAUGES, lists):
            setattr(main, gauge, list(readings))
    used = [list(getattr(main, gauge)) for gauge in GAUGES]
    try:
        with patch("builtins.input", side_effect=["JJ", str(watch)]):
            main.main()
    finally:
        for gauge, readings in original.items():
            setattr(main, gauge, readings)
    out, err = capsys.readouterr()
    assert err == "", "the program wrote to the error stream:\n" + err
    return out, used


def test_program_prints_the_same_report(capsys):
    for watch, lists in [
        (40, None),
        (20, [[5, 9, 3], [40, 20, 10, 30], [21, 22]]),
    ]:
        out, used = run(capsys, watch, lists)
        context = f"watch={watch}, readings: {used}"
        want = [expected_report(readings, watch) for readings in used]
        for position, label in enumerate(["Highest", "Reached watch", "Average"]):
            expected = [str(report[position]) for report in want]
            got = values(out, label)
            assert got == expected, (
                f'the "{label}" lines said {got}, expected {expected}, one per gauge '
                f"in the order Meadville, Saegertown, Cussewago ({context})"
            )
        peak = [str(max(max(readings) for readings in used))]
        assert values(out, "Peak") == peak, (
            f'the "Peak" line said {values(out, "Peak")}, expected {peak} ({context})'
        )


def test_highest_returns_the_largest():
    # Largest in the middle, at the end, and at the very start.
    expect_return("highest", ([12, 20, 7],), 20)
    expect_return("highest", ([12, 20, 41],), 41)
    expect_return("highest", ([55, 20, 41],), 55)


def test_count_at_or_above_returns_the_count():
    expect_return("count_at_or_above", ([10, 20, 30], 20), 2)
    # A reading exactly at the level counts.
    expect_return("count_at_or_above", ([10, 20, 30], 30), 1)
    expect_return("count_at_or_above", ([10, 20, 30], 10), 3)
    # Zero is a number, not None: start the count at 0 and return it.
    expect_return("count_at_or_above", ([10, 20, 30], 31), 0)


def test_average_returns_a_whole_number():
    # 305 // 7 is 43, where 305 / 7 would be 43.571...
    expect_return("average", ([31, 34, 52, 68, 45, 39, 36],), 43)
    expect_return("average", ([12, 20, 7],), 13)


def test_report_prints_one_gauge(capsys):
    function("report")("Test Gauge", [12, 20, 7], 15)
    out, _ = capsys.readouterr()
    call = 'report("Test Gauge", [12, 20, 7], 15)'
    for label, want in [
        ("GAUGE", "TEST GAUGE"),
        ("Highest", "20"),
        ("Reached watch", "1"),
        ("Average", "13"),
    ]:
        got = values(out, label)
        assert got == [want], f'{call} printed {got} on its "{label}" line, expected {want}'
