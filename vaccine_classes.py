"""CSC111 Final Project: Visualizing COVID-19 Vaccinations In the World
Module Description
===============================
This module contains a collection of Python classes and functions that will be used in the
other modules.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Zachary Lee.
"""
from __future__ import annotations
from typing import Optional
import datetime


class Location:
    """ A custom data type that represents vaccine and location data.
    Instance Attributes:
        - name: The name of the location.
        - identifier: If it is a country then this is the country code of the location.
        - coordinates: The latitude and longitude of the location.
        - vaccine_data: The vaccination data over an amount of time.
        - sub_locations: The countries within it if it is a continent.

    Representation Invariants:
        - isinstance(self.name, str)
        - isinstance(self.identifier, str)
        - self.vaccine_data != {}
    >>> canada = Location('Canada', [56, -106], {datetime.date(2020, 12, 15): 100}, \
    identifier='CAN')
    >>> canada.is_country()
    True
    >>> canada.get_latest_total()
    100
    """
    name: str
    identifier: Optional[str]
    coordinates: [float, float]
    vaccine_data: {datetime.date: int}
    sub_locations: list[Location]

    def __init__(self, name: str, coordinates: [float, float],
                 vaccine_data: {datetime.date: int},
                 sub_locations: Optional[list] = None,
                 identifier: Optional[str] = None) -> None:
        """Initialize a new location with the given information.

        Preconditions:
            - name != ''
        """
        if sub_locations is None:
            sub_locations = []
        self.name = name
        self.identifier = identifier
        self.coordinates = coordinates
        self.vaccine_data = vaccine_data
        self.sub_locations = sub_locations

    def is_country(self) -> bool:
        """Return True if the location is a country. False if it is a continent.
        """
        return self.identifier is not None

    def get_latest_total(self) -> int:
        """Return the latest total number of vaccinations for a specific location. If the location
        is a continent return the total of all the latest number of vaccinations in its countries.

        Preconditions:
            - self.vaccine_data != {}
        """
        if self.is_country():
            latest_entry = max(list(self.vaccine_data.keys()))
            return self.vaccine_data[latest_entry]
        else:
            total = 0

            for country in self.sub_locations:
                total += country.get_latest_total()

            return total


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
        'extra-imports': ['__future__', 'typing', 'datetime'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136', 'R0913']
    })
