"""CSC111 Final Project: Visualizing COVID-19 Vaccinations In the World
Module Description
===============================
The main module uses all the functions from the other modules to produce a visualization of the
vaccination data retrieved from the datasets.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Zachary Lee.
"""
import folium
import webbrowser
from visualize_vaccinations import add_country_data, add_continent_data, \
    add_graph_markers_continent, add_graph_markers_country
import process_vaccine_data

m = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodbpositron')
folium.TileLayer('cartodbdark_matter').add_to(m)

add_country_data('datasets/country_vaccinations.csv',
                 'datasets/countries_codes_and_coordinates.csv',
                 'datasets/countries.geojson', m)

add_continent_data('datasets/country_vaccinations.csv',
                   'datasets/countries_codes_and_coordinates.csv',
                   'datasets/country-and-continent-codes-list-csv_csv.csv',
                   'datasets/continents.json', m)

add_graph_markers_country('datasets/country_vaccinations.csv',
                          'datasets/countries_codes_and_coordinates.csv', m)

countries = process_vaccine_data.create_country_locations(
    'datasets/country_vaccinations.csv', 'datasets/countries_codes_and_coordinates.csv')

add_graph_markers_continent(countries,
                            'datasets/country-and-continent-codes-list-csv_csv.csv', m)

folium.LayerControl().add_to(m)

m.save('map.html')
webbrowser.open('map.html', new=2)
