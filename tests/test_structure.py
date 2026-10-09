"""Structure checks for Activity 6: Three Gauges.

These read `src/main.py` as Python, not as text, so the words in the TODO
comments do not count. Only real statements do.
"""

import ast
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "src" / "main.py"


def functions():
    """Every function defined in the file, by name."""
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    return {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}


def calls_in(node):
    """The names of every function called inside `node`, one entry per call."""
    return [
        n.func.id for n in ast.walk(node)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
    ]


def loops_in(node):
    return [n for n in ast.walk(node) if isinstance(n, (ast.For, ast.While))]


def test_report_calls_the_three_functions():
    defined = functions()
    assert "report" in defined, "found no function called report"
    report = defined["report"]
    called = calls_in(report)
    missing = [name for name in ["highest", "count_at_or_above", "average"] if name not in called]
    assert not missing, f"report does not call {', '.join(missing)}: it hands its readings to the three functions"
    assert not loops_in(report), "report has a loop in it: the loops belong in the three functions it calls"


def test_main_has_no_loops_and_reports_every_gauge():
    defined = functions()
    assert "main" in defined, "found no function called main"
    loops = loops_in(defined["main"])
    assert not loops, (
        f"main still has {len(loops)} loop(s) in it: replace each gauge block with a call to report"
    )
    reports = calls_in(defined["main"]).count("report")
    assert reports >= 3, f"main calls report {reports} time(s), expected one call per gauge, three in all"


def test_every_function_has_a_docstring():
    missing = [name for name, node in functions().items() if ast.get_docstring(node) is None]
    assert not missing, (
        f"no docstring in {', '.join(missing)}: the first line of a function's body is a "
        'string in triple quotes saying what it returns or prints'
    )
