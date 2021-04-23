"""CSC111 Final Project: Visualizing COVID-19 Vaccinations In the World
Module Description
===============================
This module contains functions that will read the data from the datasets.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Zachary Lee.
"""
import csv
import datetime


def read_vaccine_data(filename: str) -> {str: {datetime.date: int}}:
    """Read all the total vaccination data over time for each country in filename and store it in
    a dictionary.

    Preconditions:
        - len(filename) > 0

    >>> vaccine_dict = read_vaccine_data('datasets/country_vaccinations.csv')
    >>> vaccine_dict['AFG'][datetime.date(2021, 3, 5)]
    8200
    """
    vaccine_data = {}

    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        previous_vaccinations = 0
        for row in reader:
            # Slices the string that contains the date for that specific row
            date = row[2]
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])

            if row[3] == '':
                vaccinations = 0
            else:
                vaccinations = int(float(row[3]))

            # Keeps track of the previous total to account for empty spaces in the data
            if vaccinations != 0 or not row[1] in vaccine_data:
                previous_vaccinations = vaccinations

            # If the country is not already in the dictionary, then initialize the
            # dictionary that is mapped to it. Otherwise, update it.
            if row[1] in vaccine_data:
                vaccine_data[row[1]][datetime.date(year, month, day)] = previous_vaccinations
            else:
                vaccine_data[row[1]] = {datetime.date(year, month, day): previous_vaccinations}

    return vaccine_data


def read_continent_data(filename: str) -> {str: [str]}:
    """Read the continent name and country code from filename and store them in a dictionary.

    Preconditions:
        - len(filename) > 0

    >>> read_continent_data('datasets/country-and-continent-codes-list-csv_csv.csv') \
    ['North America'][0]
    'ATG'
    """
    continent_data = {}

    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            # If the continent is already in the dictionary then append the country to the list
            # for that continent. Otherwise, initialize a new list.
            if row[0] in continent_data:
                continent_data[row[0]].append(row[4])
            else:
                continent_data[row[0]] = [row[4]]

    return continent_data


def read_coordinate_data(filename: str) -> {str: [float, float]}:
    """Read the coordinates of each country in filename and create a dictionary of country code
    mapped to coordinates.

    Preconditions:
        - len(filename) > 0

    >>> read_coordinate_data('datasets/countries_codes_and_coordinates.csv')['AFG']
    [33.0, 65.0]
    """
    coordinates = {}

    with open(filename) as file:
        reader = csv.reader(file, skipinitialspace=True)
        next(reader)

        # This loop reads each row and maps a coordinate to the country code.
        for row in reader:
            coordinates[row[2]] = [float(row[4]), float(row[5])]

    return coordinates


def read_country_names(filename: str) -> {str: str}:
    """Read the vaccine data file and return a dictionary of country codes mapped to country names.

    Preconditions:
        - len(filename) > 0

    >>> read_country_names('datasets/country_vaccinations.csv')['AFG']
    'Afghanistan'
    """
    country_data = {}

    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            # Assigns the country name to the country code
            country_data[row[1]] = row[0]

    return country_data


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'datetime'],  # the names (strs) of imported modules
        'allowed-io': ['read_continent_data', 'read_coordinate_data', 'read_vaccine_data',
                       'read_country_names'],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
