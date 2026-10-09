"""Three Gauges.

CMPSC 100: Computational Expression, Activity 6

A week of readings from three stream gauges near Meadville, reported the same
way for each gauge. This program works, but it repeats the same code three
times. Move each calculation into a function, written once and used three
times, without changing what the program prints.

Author: TODO
"""

meadville = [31, 34, 52, 68, 45, 39, 36]
saegertown = [28, 30, 41, 57, 49, 35, 33]
cussewago = [12, 15, 22, 26, 19, 17, 14]

# TODO 1: write a function `highest(readings)` that returns the largest
# reading in the list. Its body is the `largest` loop from a gauge below,
# with `meadville` replaced by the parameter `readings`

# TODO 2: write a function `count_at_or_above(readings, level)` that returns
# how many readings are greater than or equal to `level`

# TODO 3: write a function `average(readings)` that returns the total of the
# readings divided by how many there are, using //

# TODO 4: write a function `report(gauge, readings, watch)` that prints the
# four report lines for one gauge: the line of "=", "GAUGE: {gauge}", then
# Highest, Reached watch, and Average. It calls the three functions above
# instead of looping itself

# TODO 5: give every function a docstring saying what it returns or prints,
# including main


def main():
    print("=" * 50)
    print("THREE GAUGES")
    print("=" * 50)

    name = input("What is your name? ")
    watch = int(input("What is the watch level this week? "))

    print("Field notes by", name)

    # TODO 6: replace each of the three gauge blocks below with one call to
    # report, such as report("French Creek at Meadville", meadville, watch)

    # French Creek at Meadville
    print("=" * 50)
    print("GAUGE: French Creek at Meadville")
    largest = meadville[0]
    for reading in meadville:
        if reading > largest:
            largest = reading
    count = 0
    for reading in meadville:
        if reading >= watch:
            count = count + 1
    total = 0
    for reading in meadville:
        total = total + reading
    print("Highest:", largest)
    print("Reached watch:", count)
    print("Average:", total // len(meadville))
    meadville_peak = largest

    # French Creek at Saegertown
    print("=" * 50)
    print("GAUGE: French Creek at Saegertown")
    largest = saegertown[0]
    for reading in saegertown:
        if reading > largest:
            largest = reading
    count = 0
    for reading in saegertown:
        if reading >= watch:
            count = count + 1
    total = 0
    for reading in saegertown:
        total = total + reading
    print("Highest:", largest)
    print("Reached watch:", count)
    print("Average:", total // len(saegertown))
    saegertown_peak = largest

    # Cussewago Creek
    print("=" * 50)
    print("GAUGE: Cussewago Creek")
    largest = cussewago[0]
    for reading in cussewago:
        if reading > largest:
            largest = reading
    count = 0
    for reading in cussewago:
        if reading >= watch:
            count = count + 1
    total = 0
    for reading in cussewago:
        total = total + reading
    print("Highest:", largest)
    print("Reached watch:", count)
    print("Average:", total // len(cussewago))
    cussewago_peak = largest

    # TODO 7: replace these comparisons with one call to highest, handed a
    # list of the three gauges' highest readings
    peak = meadville_peak
    if saegertown_peak > peak:
        peak = saegertown_peak
    if cussewago_peak > peak:
        peak = cussewago_peak
    print("=" * 50)
    print("Peak:", peak)


if __name__ == "__main__":
    main()
