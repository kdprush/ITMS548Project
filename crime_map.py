# crime_map.py

import requests
import folium
import webbrowser

class CrimeMap:
    def __init__(self):
        self.data_url = "https://data.cityofchicago.org/resource/dfnk-7re6.json"

    def fetch_crime_data(self):
        response = requests.get(self.data_url)
        return response.json()

    def create_map(self):
        chicago_map = folium.Map(location=[41.8781, -87.6298], zoom_start=11)
        crime_data = self.fetch_crime_data()
        for crime in crime_data:
            try:
                latitude = float(crime['latitude'])
                longitude = float(crime['longitude'])
                crime_type = crime['primary_type']  # Adjust the key here if necessary
                popup_text = f"Crime Type: {crime_type}"
                folium.Marker([latitude, longitude], popup=popup_text).add_to(chicago_map)
            except KeyError:
                # Skip this data point if 'primary_type' key is not found
                pass
        return chicago_map

    def open_chicago_map(self):
        webbrowser.open("https://data.cityofchicago.org/Public-Safety/Crimes-Map/dfnk-7re6")
