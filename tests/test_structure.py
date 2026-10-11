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


def test_main_has_no_loops():
    defined = functions()
    assert "main" in defined, "found no function called main"
    loops = loops_in(defined["main"])
    assert not loops, (
        f"main still has {len(loops)} loop(s) in it: each loop belongs in one of the "
        "functions, and main calls the function instead"
    )


def test_main_calls_each_function_for_every_gauge():
    defined = functions()
    assert "main" in defined, "found no function called main"
    called = calls_in(defined["main"])
    short = [
        f"{name} ({called.count(name)} time(s))"
        for name in ["read_readings", "highest", "count_at_or_above", "average"]
        if called.count(name) < 3
    ]
    assert not short, (
        f"main calls {', '.join(short)}: each function is called once per gauge, three times in all"
    )
