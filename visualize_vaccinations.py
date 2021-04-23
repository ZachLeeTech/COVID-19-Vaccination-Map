"""CSC111 Final Project: Visualizing COVID-19 Vaccinations In the World
Module Description
===============================
This module contains functions that will display the vaccination data in an interactive map.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Zachary Lee.
"""
import base64
import folium
import plotly.graph_objects as go
import process_vaccine_data
import vaccine_classes


def add_country_data(vaccination_filename: str, country_coordinates_filename: str,
                     country_json_filename: str, folium_map: folium.Map) -> None:
    """Add the country vaccination data to the map.

    Preconditions:
        - vaccination_filename != ''
        - country_code_filename != ''
    """
    countries = process_vaccine_data.create_country_locations(
        vaccination_filename, country_coordinates_filename)
    country_dictionary = {country.identifier: country.get_latest_total() // 1000000 for country
                          in countries}
    country_geo = country_json_filename

    folium.Choropleth(
        geo_data=country_geo,
        name="Country Level Choropleth",
        data=country_dictionary,
        columns=["Country", "Total Vaccinations"],
        key_on="feature.properties.ISO_A3",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name="Country Level Total Vaccinations (In Millions)",
        show=False).add_to(folium_map)


def add_continent_data(vaccination_filename: str, country_coordinates_filename: str,
                       continent_filename: str, continent_json_filename: str,
                       folium_map: folium.Map) -> None:
    """Add the continent vaccination data to the map.

    Preconditions:
        - vaccination_filename != ''
        - country_code_filename != ''
    """
    countries = process_vaccine_data.create_country_locations(
        vaccination_filename, country_coordinates_filename)
    continents = process_vaccine_data.create_continent_locations(countries, continent_filename)

    continent_dictionary = {continent.name: continent.get_latest_total() // 1000000 for
                            continent in continents}

    continent_geo = continent_json_filename

    folium.Choropleth(
        geo_data=continent_geo,
        name="Continental Choropleth",
        data=continent_dictionary,
        columns=["Continent", "Total Vaccinations"],
        key_on="feature.properties.continent",
        fill_color="OrRd",
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name="Continental Total Vaccinations (In Millions)").add_to(folium_map)


def add_graph_markers_country(vaccine_filename: str, coordinate_filename: str,
                              folium_map: folium.Map) -> None:
    """Use plotly to generate graphs for each country and add markers for each graph to the map.

    Preconditions:
        - vaccine_filename != ''
        - coordinate_filename != ''
    """
    countries = process_vaccine_data.create_country_locations(vaccine_filename,
                                                              coordinate_filename)
    feature_group = folium.FeatureGroup(name='Country Level Markers and Graphs')
    for country in countries:
        dates = list(country.vaccine_data.keys())
        dates.sort()
        total_vaccinations = []

        for date in dates:
            total_vaccinations.append(country.vaccine_data[date])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=total_vaccinations))
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Total Vaccinations')
        title = f'Total Vaccinations in {country.name} Over Time'
        fig.update_layout(title_text=title)
        jpg = 'datasets/graph.jpg'
        fig.write_image(file=jpg, format='jpg', width=500, height=410)

        encoded = base64.b64encode(open(jpg, 'rb').read())

        html = '<img src="data:image/jpg;base64,{}">'.format

        iframe = folium.IFrame(html(encoded.decode('UTF-8')), width='510px', height='430px')
        feature_group.add_child(folium.Marker(location=country.coordinates,
                                              popup=folium.Popup(iframe, max_width=2650),
                                              icon=folium.Icon(icon='flag')))
    folium_map.add_child(feature_group)


def add_graph_markers_continent(countries: [vaccine_classes.Location],
                                continent_filename: str, folium_map: folium.Map) -> None:
    """Use plotly to generate graphs for each continent and add markers for each graph to the map.

    Preconditions:
        - vaccine_filename != ''
        - coordinate_filename != ''
    """
    continents = process_vaccine_data.create_continent_locations(countries, continent_filename)

    feature_group = folium.FeatureGroup(name='Continental Markers and Graphs')
    for continent in continents:
        if continent.vaccine_data != {}:
            dates = list(continent.vaccine_data.keys())
            dates.sort()
            total_vaccinations = []

            for date in dates:
                total_vaccinations.append(continent.vaccine_data[date])

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=total_vaccinations))
            fig.update_xaxes(title_text='Date')
            fig.update_yaxes(title_text='Total Vaccinations')
            title = f'Total Vaccinations in {continent.name} Over Time'
            fig.update_layout(title_text=title)
            fig.write_image(file='datasets/graph.jpg', format='jpg', width=500, height=410)

            encoded = base64.b64encode(open('datasets/graph.jpg', 'rb').read())

            html = '<img src="data:image/jpg;base64,{}">'.format

            iframe = folium.IFrame(html(encoded.decode('UTF-8')), width='510px', height='430px')
            feature_group.add_child(folium.Marker(location=continent.coordinates,
                                                  popup=folium.Popup(iframe, max_width=2650),
                                                  icon=folium.Icon(icon='globe', color='red')))
    folium_map.add_child(feature_group)


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
        'extra-imports': ['folium', 'process_vaccine_data', 'webbrowser', 'plotly.graph_objects',
                          'base64', 'vaccine_classes'],
        # the names (strs) of imported modules
        'allowed-io': ['add_graph_markers_country', 'add_graph_markers_continent'],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
