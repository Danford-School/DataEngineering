import csv
import pandas as pd
import math


def find_null(column):
    data = pd.read_csv('crashdata.csv')
    is_there_a_blank = False
    for n in data[column]:
        if math.isnan(n):
            is_there_a_blank = True
    print("Does " + column + " contain null values: " + str(is_there_a_blank))


# find_null("Vehicle ID")
# find_null("Crash ID")
# find_null("Record Type")


def count_days():
    data2 = pd.read_csv('crashdata.csv')
    monday = 0
    tuesday = 0
    wednesday = 0
    thursday = 0
    friday = 0
    saturday = 0
    sunday = 0
    for n in data2['Week Day Code']:
        print(n)
        if n == 1:
            sunday += 1
        if n == 2:
            monday += 1
        if n == 3:
            tuesday += 1
        if n == 4:
            wednesday += 1
        if n == 5:
            thursday += 1
        if n == 6:
            friday += 1
        if n == 7:
            saturday += 1
    print("Monday: " + str(monday))
    print("Tuesday: " + str(tuesday))
    print("Wednesday: " + str(wednesday))
    print("Thursday: " + str(thursday))
    print("Friday: " + str(friday))
    print("Saturday: " + str(saturday))
    print("Sunday: " + str(sunday))


# count_days()


def check_numbers_within(column, low, high):
    data3 = pd.read_csv('crashdata.csv')
    for n in data3[column]:
        if math.isnan(n):
            continue
        if column == "Crash Hour" and n == 99:
            continue
        m = int(n)
        if m > high or m < low:
            print("OUT OF RANGE!!! " + column + ": " + str(m))
    print("If there is nothing above this line, then everything is fine.\n\nI'm a poet and I was not aware!")


# check_numbers_within("Crash Day", 1, 31)
# check_numbers_within("County Code", 1, 36)
# check_numbers_within("Crash Month", 1, 12)
# check_numbers_within("Crash Hour", 0, 23)


def check_if_exists_in_all_tables(column, value):
    data4 = pd.read_csv('crashdata.csv')
    crash_data_1 = data4[data4['Record Type'] == 1]
    crash_data_2 = data4[data4['Record Type'] == 2]
    crash_data_3 = data4[data4['Record Type'] == 3]

    for n in crash_data_1[column]:
        if n == value:
            for nn in crash_data_2[column]:
                if nn == value:
                    for nnn in crash_data_3[column]:
                        if nnn == value:
                            print(str(value) + " exists in all tables! ")
                            break
                        else:
                            print(str(value) + " does not exist in table 3. :(")
                            break
                    break
                else:
                    print(str(value) + " does not exist in table 2. :(")
                    break
            break
        else:
            print(str(value) + " does not exist in table 1. :(")
            break


# check_if_exists_in_all_tables("Crash ID", 1809119)


def check_unique(column):
    data4 = pd.read_csv('crashdata.csv')
    flag = 0
    flag = len(set(data4[column])) == len(data4[column])
    if flag:
        print("Column is unique!")
    else:
        print("Column is not unique! :(")


check_unique("Crash ID")
