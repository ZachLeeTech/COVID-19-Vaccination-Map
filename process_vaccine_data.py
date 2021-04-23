"""CSC111 Final Project: Visualizing COVID-19 Vaccinations In the World
Module Description
===============================
This module contains functions that will process the data obtained using the functions in
read_vaccine_data.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Zachary Lee.
"""
import datetime
import read_data
import vaccine_classes

CONTINENT_COORDINATES = {'North America': [54.5260, -105.2551],
                         'South America': [-8.7832, -55.4915],
                         'Africa': [-8.7832, 34.5085], 'Oceania': [-22.7359, 140.0188],
                         'Antarctica': [-82.8628, 135], 'Asia': [34.0479, 100.6197],
                         'Europe': [54.5260, 15.2551]}


def create_country_locations(vaccine_filename: str, coordinate_filename: str) \
        -> [vaccine_classes.Location]:
    """Read the data from the vaccine dataset and the country coordinate dataset and create a
    Location instance for each country.

    Preconditions:
        - len(vaccine_filename) > 0
        - len(coordinate_filename) > 0

    >>> create_country_locations('datasets/country_vaccinations.csv', \
    'datasets/countries_codes_and_coordinates.csv')[0].name
    'Afghanistan'
    """
    vaccine_data = read_data.read_vaccine_data(vaccine_filename)
    coordinate_data = read_data.read_coordinate_data(coordinate_filename)
    country_codes = read_data.read_country_names(vaccine_filename)
    location_list = []

    for country in vaccine_data:
        if country in coordinate_data:
            location = vaccine_classes.Location(country_codes[country], coordinate_data[country],
                                                vaccine_data[country], identifier=country)

            location_list.append(location)

    return location_list


def create_continent_locations(countries: [vaccine_classes.Location], continent_filename: str)\
        -> [vaccine_classes.Location]:
    """Return a list containing the continent location instances.

    Preconditions:
        - countries != []
        - continent_filename != ''

    >>> country_locations = create_country_locations('datasets/country_vaccinations.csv', \
    'datasets/countries_codes_and_coordinates.csv')
    >>> create_continent_locations(country_locations, \
    'datasets/country-and-continent-codes-list-csv_csv.csv')[0].name
    'Asia'
    """
    continent_data = read_data.read_continent_data(continent_filename)
    continent_list = []

    for continent in continent_data:
        country_list = continent_data[continent]
        sub_locations = [country for country in countries if country.identifier in country_list]
        new_vaccine_data = sum_continent_vaccinations(sub_locations)
        continent_list.append(vaccine_classes.Location(continent, CONTINENT_COORDINATES[continent],
                                                       new_vaccine_data, sub_locations))

    return continent_list


def sum_continent_vaccinations(countries: [vaccine_classes.Location]) -> {datetime.date: int}:
    """Return a dictionary of dates mapped to total vaccinations for the continent.

    Preconditions:
        - countries != []

    >>> country_locations = create_country_locations('datasets/country_vaccinations.csv', \
    'datasets/countries_codes_and_coordinates.csv')
    >>> continent_locations = create_continent_locations(country_locations, \
    'datasets/country-and-continent-codes-list-csv_csv.csv')
    >>> sum_continent_vaccinations(continent_locations[0].sub_locations) \
    [datetime.date(2020, 12, 15)]
    1528500
    """
    dates = set()
    for country in countries:
        for date in country.vaccine_data:
            dates.add(date)

    dates = list(dates)
    dates.sort()
    new_vaccination_total = {current_date: 0 for current_date in dates}

    for country in countries:
        prev_total = 0
        for date in dates:
            if date in country.vaccine_data:
                new_vaccination_total[date] += country.vaccine_data[date]
                prev_total = country.vaccine_data[date]
            else:
                new_vaccination_total[date] += prev_total

    return new_vaccination_total


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
        'extra-imports': ['read_data', 'vaccine_classes', 'datetime'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
