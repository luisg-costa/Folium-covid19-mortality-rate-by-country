import folium
import pandas

covid_data = pandas.read_json('data/covid19data.json')
covid_data = covid_data['features'].apply(pandas.Series)
covid_data = covid_data['attributes'].apply(pandas.Series)

latitude = covid_data['Lat']
longitude = covid_data['Long_']
country_name = covid_data["Country_Region"]
mortality = covid_data['Mortality_Rate']

html_covid = """<h4>Information:</h4>
Name: {} <br>
Mortality Rate: {}
"""


def color_rate(rate):
    if rate < 1:
        return 'green'
    elif 1 <= rate < 2:
        return 'orange'
    else:
        return 'red'


map = folium.Map(location=[38.50, -99.09], zoom_start=5, tiles="Stamen Terrain")

fg_covid_mortality = folium.FeatureGroup(name='Covid Mortality Rate')

for lat, lon, name, mort in zip(latitude, longitude, country_name, mortality):
    iframe = folium.IFrame(html=html_covid.format(name, round(mort, 2)), width=200, height=100)
    fg_covid_mortality.add_child(
        folium.CircleMarker(location=[lat, lon], popup=folium.Popup(iframe), fill_color=color_rate(mort),
                            fill_opacity=1, color='grey', radius=6))

map.add_child(fg_covid_mortality)

map.add_child(folium.LayerControl())

map.save('Map_mortality_rate.html')
