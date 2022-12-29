import folium
import pandas as pd
from folium import plugins
import seaborn as sns
import matplotlib.pyplot as plt

bikes = pd.read_csv('indego-trips-2022-q2.csv')
bikes

#deleting missing values
bikes = bikes.dropna()

#combining the start and end stations, latitude, and longitude
station = pd.DataFrame(bikes[['start_station','end_station']].stack(dropna=True),columns=['station']).reset_index(level=1, drop=True)
pd.merge(bikes[['start_station']],station,how='left',left_index=True, right_index=True)

lat = pd.DataFrame(bikes[['start_lat','end_lat']].stack(dropna=True),columns=['lat']).reset_index(level=1, drop=True)
pd.merge(bikes[['start_lat']],lat,how='left',left_index=True, right_index=True)

long = pd.DataFrame(bikes[['start_lon','end_lon']].stack(dropna=True),columns=['long']).reset_index(level=1, drop=True)
pd.merge(bikes[['start_lon']],long,how='left',left_index=True, right_index=True)

bikes = pd.concat([station, lat, long], axis=1)

#removing duplicates with a function to see total number of stations 
def remove_dup_rows(df):
    df_row = df.drop_duplicates()
    return df_row
stations = remove_dup_rows(bikes)

#making base map
map = folium.Map(location=[39.9526, -75.1652])

#adding station coordinates to base map
#this is a basic map showing the station pinpoints; the interactive map is below
for i in range(0,len(stations)):
       folium.Marker(
      location=[stations.iloc[i]['lat'], stations.iloc[i]['long']],
   ).add_to(map)

#importing csv that contains stations names and numbers 
names = pd.read_csv('indego-stations-2022-10-01.csv')

names = names.drop(columns = ['Day of Go_live_date', 'Status'])

#joining the two dataframes 
stations = stations.rename(columns = {"station":"Station_ID"})
combined = pd.merge(stations, names, on='Station_ID', how='inner')

#base map again
map = folium.Map(location=[39.9526, -75.1652])

#adding station coordinates, names, and bike logo to pinpoints
for i in range(0,len(combined)):
   folium.Marker(
      location=[combined.iloc[i]['lat'], combined.iloc[i]['long']],
      popup=combined.iloc[i]['Station_Name'],
      icon=folium.Icon(icon='bicycle', prefix = 'fa'),
   ).add_to(map)
map

#exporting map to html
map.save("bike_station_map.html")

