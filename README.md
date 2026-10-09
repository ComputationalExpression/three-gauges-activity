# Activity 6: Three Gauges

|Item |       |
|:----|:------|
|Released |Wednesday, October 21, in class |
|Due |Monday, October 26, 9:50am |
|Progress |[![Grade](../../actions/workflows/main.yml/badge.svg?branch=main)](../../actions/workflows/main.yml) |

Cussewago Creek meets French Creek in Meadville. This program reports a week of readings from
three gauges: French Creek at Meadville, French Creek upstream at Saegertown, and Cussewago
Creek. It already works, but it repeats the same loops three times, once per gauge. Your job is
to **refactor** it, which means changing how the code is organized without changing what it
prints: move each calculation into a function, written once and called three times.

Everything here comes from the Week 9 Functions slides and the weeks before them. If a step
confuses you, please ask about it while you are still in the room.

## Course learning outcomes

This activity addresses the following course learning outcomes:

**CLO 1.** Apply Python programming fundamentals to execute and explain computer code that
implements interactive, novel solutions to a variety of computable problems.

**CLO 3.** Analyze and suggest revisions to existing Python code to add functionality or repair
defects.

Specifically, by the end of this activity you should be able to:

* define a function with parameters
* return a value from a function, and use the value it returns
* tell `return` apart from `print`
* replace repeated code with calls to one function

## The functions

Write these three functions above `main`. The names and parameters must match exactly, because
the automated checks call each one directly with readings of their own.

|Function |What it does |
|:--------|:------------|
|`highest(readings)` |Returns the largest reading in the list |
|`count_at_or_above(readings, level)` |Returns how many readings are greater than or equal to `level` |
|`average(readings)` |Returns the total of the readings divided by how many there are, using `//` |

Each function **returns** its answer and prints nothing; `main` does the printing. Each one
works only with its parameters, never with `meadville`, `saegertown` or `cussewago` by name.

Then, in each gauge block in `main`, delete the three loops and print what your functions return
instead, such as `print("Highest:", highest(meadville))`. Replace the `peak` comparisons with one
call to `highest`, handed a list of the three gauges' highest readings. When you are done, `main`
has no loops in it.

### Example run

The program prints the same thing before and after the refactor:

```text
$ uv run python src/main.py
==================================================
THREE GAUGES
==================================================
What is your name? JJ
What is the watch level this week? 40
Field notes by JJ
==================================================
GAUGE: French Creek at Meadville
Highest: 68
Reached watch: 3
Average: 43
==================================================
GAUGE: French Creek at Saegertown
Highest: 57
Reached watch: 3
Average: 39
==================================================
GAUGE: Cussewago Creek
Highest: 26
Reached watch: 0
Average: 17
==================================================
Peak: 68
```

The readings are sample data. The checks forgive extra spaces and letter case, and any of the
three ways to print a value passes.

## Getting started

Open `src/main.py` and work through the `TODO` markers in order. Run the program after each
function you write, and check that it still prints the report above:

```text
uv run python src/main.py
```

Put your name on the `Author:` line at the top of the file, and delete each `TODO` marker as
you finish that step.

## Evaluation

In-class activities are graded on completion and contribute to the **In-Class Activities**
category on the syllabus (10 points, averaged across the semester). This activity is worth one
activity grade. What is graded is the attempt, not whether every value comes out right.

|Level |What it looks like |
|:-----|:------------------|
|**Complete** |At least half of the activity is done |
|**Partial** |Less than half is done, but something beyond the starter was committed |
|**Incomplete** |Nothing was changed |

Run the automated checks yourself, as many times as you like, from the top folder of this
repository rather than from inside `src`:

```text
uv run gatorgrade --config gatorgrade.yml
```

Each check's description says what to look at when it fails. Under a failed check, gatorgrade
also prints a `uv run pytest ...` command. Run it: the last lines name the function that was
called, what it returned, and what was expected.

> [!NOTE]
> Automated results are preliminary. Your instructor sets the final grade.

## Submitting

Commit and push often. The last version pushed before the deadline is the one that gets
graded.

**In the terminal:**

```text
git add src/main.py
git commit -m "Refactor the gauge report into functions"
git push
```

**In VS Code**, the Source Control panel in the left sidebar does the same three steps:

1. Click **+** next to a changed file to stage it, which is `git add`
2. Type a message in the box at the top, then click the checkmark, which is `git commit`
3. Click **Sync Changes** (or the up arrow) to push

Either way, then open your repository on GitHub and confirm your latest changes are actually
there.

If you need more time, apply a late token with [this form](https://forms.gle/3nGbpaNrG96DpLLdA).
