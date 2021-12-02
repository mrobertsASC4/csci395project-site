## The Effect of the Lack of Health Clinics on Homelessness

Watching the news and through everyday observation, there has been an increase in homelessness in neighborhoods that have limited access to health clinics, shelters and 
services. I am going to use my project to display the correlation between the number of mental health clinics in neighborhoods and the rate of homelessness, while also delving deeper and looking into specific areas/districts in the neighborhood and their homelessness rate, and compare them to its attendance in new people looking for shelter and the amount of homeless individuals that reside in shelters in the area, even with the clinics availaible. This data, in turn, would further my current solution to facilitate more health clinics in areas with a high rate of impoverishment, so that more individuals would start to reside in shelters.

I downloaded the data I obtained as CSV files and have read them in as separate Dataframes. I have used pandas and its functions to use specific columns I need for my data. For starters, I started with my data on Homelessness Numbers from 2009-2012. This is how I parsed it to use what I needed:

```
homeless_roster = pd.read_csv('Directory_Of_Homeless_Population_By_Year.csv')
homeless_roster['Borough'] = homeless_roster['Area']

homeless_query = 'SELECT * FROM homeless_roster WHERE Year == 2011 GROUP BY Borough'
selected_Homeless_Year = psql.sqldf(homeless_query)
newDF = pd.DataFrame(selected_Homeless_Year)
```
_What I did here was make a new column "Borough" for the column "Area". This will be used to combine with the other Dataframe of health clinics, and to select what I need for my data through SQL. This specific query selects all of the data from homeless_roster where the year is 2011. I then group this data by the boroughs. This is the result:_

```
   Year            Area  Homeless Estimates         Borough
0  2011          Bronx                  115           Bronx
1  2011       Brooklyn                  242        Brooklyn
2  2011      Manhattan                  786       Manhattan
3  2011         Queens                  102          Queens
4  2011  Staten Island                  128   Staten Island
```

Next, I did something similar to my health clinic data:
```
healthclinics_roster = pd.read_csv('NYC_Health_Hospitals_patient_care_locations_2011.csv')

health_query = 'SELECT COUNT(Borough) AS numClinics, Borough FROM healthclinics_roster GROUP BY Borough'
selected_Health = psql.sqldf(health_query)
newDF2 = pd.DataFrame(selected_Health)
```

_Here, I select the borough count for each item in healthclinics_roster, and rename it as numClinics. Then, I also select the Borough and group this data by the borough. This is the result:_

```
   numClinics        Borough
0          14          Bronx
1          26       Brooklyn
2          24      Manhattan
3          11         Queens
4           3  Staten Island
```

Using these sets of data, I did an inner join on both tables on their corresponding column, Borough. This is the code and its result.
```
newSomething = newDF.merge(newDF2, left_index=True, right_index=True, how='inner')
print(newSomething)

   Year           Area  Homeless Estimates      Borough_x  numClinics      Borough_y
0  2011          Bronx                 115          Bronx          14          Bronx
1  2011       Brooklyn                 242       Brooklyn          26       Brooklyn
2  2011      Manhattan                 786      Manhattan          24      Manhattan
3  2011         Queens                 102         Queens          11         Queens
4  2011  Staten Island                 128  Staten Island           3  Staten Island
```
_Note: The Health Clinic Data is also centered in the year 2011._

I do not know why the table ends up like this. I am trying to fix it on my end, but this is the outcome I have at the moment and it works. I want to use this table data to create a bar graph or a line graph to show the correlation between Homeless Estimates and numClinics in each borough. Through this, you would be able to see which borough has the most homeless estimates for the year of 2011 and the number of clinics in that borough as well, to prove my assumption that the lower the amount of clinics in a borough, the higher amount of homeless individuals there will be.

Secondly, I created a map to display the previous sets of data using folium. This is how I did it:
```
import folium

#showing location of health clinics
health_clinic_locations = healthclinics_roster[['Latitude' , 'Longitude', 'Facility Name']]
select_non_empty = health_clinic_locations.loc[health_clinic_locations['Latitude'].notna()]


centerOfHunter = [40.7678,-73.9645]
nyc_clinic_map_2011 = folium.Map(location=centerOfHunter, zoom_start=10, scale=13)

for ix, clinic_info in select_non_empty.iterrows():
    folium.Marker([clinic_info['Latitude'], clinic_info['Longitude']], popup=clinic_info['Facility Name']).add_to(nyc_clinic_map_2011)

#bronx 2011 homeless
folium.Marker(
    location=[40.8448, -73.8648],
    popup="Total Number of Bronx Clinics in 2011: " + str(newSomething.loc[0, 'numClinics']),
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(nyc_clinic_map_2011)

folium.CircleMarker(
    location=[40.8448, -73.8648],
    radius=50,
    popup="Total Bronx Homeless Population in 2011: " + str(newDF.loc[0, 'Homeless Estimates']),
    color="#3186cc",
    fill=True,
    fill_color="#3186cc",
).add_to(nyc_clinic_map_2011)

etc...
```
_This centers the map on Hunter's location. Then, I create a map using folium, and created markers to represent each clinic using its Latitude and Longitute values. Next, I created specific markers for each borough and its respective latitude and longitude. The Circle markers show the total homeless population of each borough and the Red markers represent the Total Number of Clinics in the borough as well. This is shown through an .html file shown below._

[Map of Clinic Locations and Total Homeless Individuals](clinic_homeless_2011.html)

This map gives a visual representation of where the clinics are in NYC and shows the respective total amounts of homeless individuals and clinics in the specific borough.

This is what I have so far, but I plan to include more analysis and visualizations once I get more of this data to use and cooperate with.
