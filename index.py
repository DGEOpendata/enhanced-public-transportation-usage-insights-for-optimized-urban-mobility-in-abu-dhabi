python
import pandas as pd
import geopandas as gpd
import folium
from flask import Flask, render_template

# Load the public transportation dataset
transport_data = pd.read_csv('abu_dhabi_public_transport.csv')

# Load geographic data for visualization
geo_routes = gpd.read_file('bus_routes.geojson')
geo_stops = gpd.read_file('bus_stops.geojson')

# Create a Flask app
app = Flask(__name__)

@app.route('/')
def home():
    # Prepare data for visualization
    map = folium.Map(location=[24.4539, 54.3773], zoom_start=12)

    # Add bus stops to the map
    for _, stop in geo_stops.iterrows():
        folium.Marker(
            location=[stop.geometry.y, stop.geometry.x],
            popup=f"Stop: {stop['stop_name']}\nUsage: {stop['daily_ridership']}"
        ).add_to(map)

    # Add bus routes to the map
    folium.GeoJson(geo_routes, name='Bus Routes').add_to(map)
    
    # Save the map to an HTML file
    map.save('templates/map.html')

    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
