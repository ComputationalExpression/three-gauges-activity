"""Three Gauges.

CMPSC 100: Computational Expression, Activity 6

A week of readings from three stream gauges near Meadville, read from one CSV
file per gauge and reported the same way for each gauge. This program works,
but it repeats the same loops three times. Move each one into a function,
written once and called three times, without changing what the program prints.

Author: TODO
"""

# TODO 1: write a function `read_readings(filename)` that returns the list of
# levels in that CSV file. Its body is the reading loop from a gauge below,
# with "data/meadville.csv" replaced by the parameter `filename`

# TODO 2: write a function `highest(readings)` that returns the largest
# reading in the list. Its body is the `largest` loop from a gauge below,
# with `meadville` replaced by the parameter `readings`

# TODO 3: write a function `count_at_or_above(readings, level)` that returns
# how many readings are greater than or equal to `level`

# TODO 4: write a function `average(readings)` that returns the total of the
# readings divided by how many there are, using //

# Each function returns its answer and prints nothing. main does the printing


def main():
    print("=" * 50)
    print("THREE GAUGES")
    print("=" * 50)

    name = input("What is your name? ")
    watch = int(input("What is the watch level this week? "))

    print("Field notes by", name)

    # TODO 5: in each gauge block below, replace the reading loop with one call
    # to read_readings, such as meadville = read_readings("data/meadville.csv").
    # Then delete the other three loops and the variables they fill, and print
    # what your functions return instead, such as
    # print("Highest:", highest(meadville)). Keep the two lines that print "="
    # and the gauge's name

    # French Creek at Meadville
    meadville = []
    with open("data/meadville.csv") as file:
        file.readline()
        for line in file:
            parts = line.split(",")
            meadville.append(int(parts[1]))
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
    saegertown = []
    with open("data/saegertown.csv") as file:
        file.readline()
        for line in file:
            parts = line.split(",")
            saegertown.append(int(parts[1]))
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
    cussewago = []
    with open("data/cussewago.csv") as file:
        file.readline()
        for line in file:
            parts = line.split(",")
            cussewago.append(int(parts[1]))
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

    # TODO 6: replace these comparisons with one call to highest, passing it a
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
