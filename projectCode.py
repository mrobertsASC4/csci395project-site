#Name: Matthew Roberts
#Email: Matthew.Roberts66@myhunter.cuny.edu
#Date: December 9th, 2021

#URL: https://mrobertsasc4.github.io/csci395project-site/
#Title: The Effect of the Number of Health Clinics on Homelessness
#Resources: Used python.org as a reminder of Python 3 print statements
#Lecture Recordings and Notes / Textbook
#https://data.cityofnewyork.us/Social-Services/Directory-Of-Homeless-Population-By-Year/5t4n-d72c
#https://data.cityofnewyork.us/Health/NYC-Health-Hospitals-patient-care-locations-2011/f7b6-v6v3
#https://www.coalitionforthehomeless.org/wp-content/uploads/2021/11/NYC_Homeless_Shelter_Population-Worksheet_1983-9-202121.pdf
#https://data.cityofnewyork.us/Social-Services/Individual-Census-by-Borough-Community-District-an/veav-vj3r
#https://data.cityofnewyork.us/Social-Services/Buildings-by-Borough-and-Community-District/3qem-6v3v
#https://data.cityofnewyork.us/Social-Services/DHS-Daily-Report/k46n-sa2m
#https://www.kite.com/python/answers/how-to-append-an-item-to-a-pandas-series-in-python
#https://stackoverflow.com/questions/25792086/pandas-merge-return-empty-dataframe
#https://thispointer.com/python-how-to-check-if-an-item-exists-in-list-search-by-value-or-condition/
#https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
#https://www.w3schools.com/sql/sql_groupby.asp
#https://www.analyticsvidhya.com/blog/2020/02/joins-in-pandas-master-the-different-types-of-joins-in-python/
#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html#pandas.DataFrame.merge
#https://www.sqlshack.com/how-to-write-sql-queries-with-spaces-in-column-names/
#https://stackoverflow.com/questions/25146121/extracting-just-month-and-year-separately-from-pandas-datetime-column?rq=1
#https://towardsdatascience.com/creating-a-simple-map-with-folium-and-python-4c083abfff94
#https://www.pluralsight.com/guides/map-visualizations-in-python-using-folium
#Previous Homework Assignments

import numpy as np
#from numpy import NaN, nan
import pandas as pd
import pandasql as psql
import folium
import matplotlib.pyplot as plt
import matplotlib.style as style

#Reading the data into their respective dataframes
homeless_roster = pd.read_csv('Directory_Of_Homeless_Population_By_Year.csv')
healthclinics_roster = pd.read_csv('NYC_Health_Hospitals_patient_care_locations_2011.csv')
homelessInShelter_roster = pd.read_csv('Individual_Census_by_Borough_Community_District_and_Facility_Type.csv')

#Adding a new column 'Borough' to use for merging data tables later
homeless_roster['Borough'] = homeless_roster['Area']

#This query selects all from the homeless_roster DataFrame where the year is equal to 2011. It is grouped by Borough.
homeless_query = 'SELECT * FROM homeless_roster WHERE Year == 2011 GROUP BY Borough'
selected_Homeless_Year = psql.sqldf(homeless_query)
newDF = pd.DataFrame(selected_Homeless_Year)
#print(newDF)


#This query selects the count of the boroughs as the number of clinics and borough from the healthclinics_roster DataFrame and groups them by Borough.
health_query = 'SELECT COUNT(Borough) AS numClinics, Borough FROM healthclinics_roster GROUP BY Borough'
selected_Health = psql.sqldf(health_query)
newDF2 = pd.DataFrame(selected_Health)
#print(newDF2)


#display this on a graph of some sort??
#this is where I merge the two Dataframes I created above using an inner join, because these tables both have the column 'Borough'
newSomething = newDF.merge(newDF2, left_index=True, right_index=True, how='inner')
#print(newSomething)

#This changes the Date in the 3rd Dataset I created into just its year, as the column 'Year' is also used in other Dataframes
homelessInShelter_roster['Report Date'] = pd.DatetimeIndex(homelessInShelter_roster['Report Date']).year

#This query selects the sums of the Individual Adult Shelter types and groups them by the borough and the date. It also orders the results by the date in ascending order. 
shelter_query = 'SELECT (SUM("Adult Family Shelter") + SUM("Adult Shelter") + SUM("Adult Shelter Commercial Hotel")) AS totalIndividuals, "Report Date" AS Year, Borough FROM homelessInShelter_roster GROUP BY Borough, "Report Date" ORDER BY "Report Date"'
selected_shelter = psql.sqldf(shelter_query)
#print(selected_shelter)
newDF3 = pd.DataFrame(selected_shelter)


#this piece of code is being used for showing the location of the health clinics; I selected the fields that were not empty, to get more accurate results and no null/na values
health_clinic_locations = healthclinics_roster[['Latitude' , 'Longitude', 'Facility Name']]
select_non_empty = health_clinic_locations.loc[health_clinic_locations['Latitude'].notna()]


#This is the beginning of the map I created using Folium. I centered the map at Hunter's Location and loaded the points on the map using a loop to iterate through
#select_non_empty and place Markers on the right latitude and longitude of the map
centerOfHunter = [40.7678,-73.9645]
nyc_clinic_map_2011 = folium.Map(location=centerOfHunter, zoom_start=10, scale=13)

for ix, clinic_info in select_non_empty.iterrows():
    folium.Marker([clinic_info['Latitude'], clinic_info['Longitude']], popup=clinic_info['Facility Name']).add_to(nyc_clinic_map_2011)

#bronx 2011 clinics
folium.Marker(
    location=[40.8448, -73.8648],
    popup="Total Number of Bronx Clinics in 2011: " + str(newSomething.loc[0, 'numClinics']),
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(nyc_clinic_map_2011)

#bronx 2011 homeless
folium.CircleMarker(
    location=[40.8448, -73.8648],
    radius=50,
    popup="Total Bronx Homeless Population in 2011: " + str(newDF.loc[0, 'Homeless Estimates']),
    color="#3186cc",
    fill=True,
    fill_color="#3186cc",
).add_to(nyc_clinic_map_2011)

#brooklyn 2011 clinics
folium.Marker(
    location=[40.6782, -73.9442],
    popup="Total Number of Brooklyn Clinics in 2011: " + str(newSomething.loc[1, 'numClinics']),
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(nyc_clinic_map_2011)

#brooklyn 2011 homeless
folium.CircleMarker(
    location=[40.6782, -73.9442],
    radius=50,
    popup="Total Brooklyn Homeless Population in 2011: " + str(newDF.loc[1, 'Homeless Estimates']),
    color="#31ccc7",
    fill=True,
    fill_color="#31ccc7",
).add_to(nyc_clinic_map_2011)

#manhattan 2011 clinics
folium.Marker(
    location=[40.7831, -73.9712],
    popup="Total Number of Manhattan Clinics in 2011: " + str(newSomething.loc[2, 'numClinics']),
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(nyc_clinic_map_2011)

#manhattan 2011 homeless
folium.CircleMarker(
    location=[40.7831, -73.9712],
    radius=50,
    popup="Total Manhattan Homeless Population in 2011: " + str(newDF.loc[2, 'Homeless Estimates']),
    color="#31cc48",
    fill=True,
    fill_color="#31cc48",
).add_to(nyc_clinic_map_2011)

#queens 2011 clinics
folium.Marker(
    location=[40.7282, -73.7949],
    popup="Total Number of Queens Clinics in 2011: " + str(newSomething.loc[3, 'numClinics']),
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(nyc_clinic_map_2011)

#queens 2011 homeless
folium.CircleMarker(
    location=[40.7282, -73.7949],
    radius=50,
    popup="Total Queens Homeless Population in 2011: " + str(newDF.loc[3, 'Homeless Estimates']),
    color="#a5cc31",
    fill=True,
    fill_color="#a5cc31",
).add_to(nyc_clinic_map_2011)

#staten island 2011 clinics
folium.Marker(
    location=[40.5795, -74.1502],
    popup="Total Number of Staten Island Clinics in 2011: " + str(newSomething.loc[4, 'numClinics']),
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(nyc_clinic_map_2011)

#staten island 2011 homeless
folium.CircleMarker(
    location=[40.5795, -74.1502],
    radius=50,
    popup="Total Staten Island Homeless Population in 2011: " + str(newDF.loc[4, 'Homeless Estimates']),
    color="#cca831",
    fill=True,
    fill_color="#cca831",
).add_to(nyc_clinic_map_2011)

nyc_clinic_map_2011.save('clinic_homeless_2011.html')

#I gathered specific columns of data needed for my bar graph in order to get accurate results.
homelessBoroDF_borough = homeless_roster['Borough']
homelessBoroDF_homelessEst = homeless_roster['Homeless Estimates']
homelessBoroDF_year = ['2009', '2010', '2011', '2012']

#This query selects the borough and the sum of the homeless estimates from the homeless_roster Dataframe and groups it by Borough
homelessEst_query = 'SELECT Borough, sum("Homeless Estimates") as totalNumofEstimates FROM homeless_roster GROUP BY Borough'
selected_HomelessEst_Year = psql.sqldf(homelessEst_query)
testing = pd.DataFrame(selected_HomelessEst_Year)
#print(testing)
#print(list(testing['Borough']))

#Styling the Graph
X_axis = np.arange(5)
width = 0.20

#This is where I brute-forced the data to get the correct information. I did this by making queries to select everything from my first Dataframe
#corresponding to a specific year. 
allHomeless = 'SELECT Year, Borough, "Homeless Estimates" FROM homeless_roster'
selected_all_homeless = psql.sqldf(allHomeless)
allHomelessData = pd.DataFrame(selected_all_homeless)
print(allHomelessData)

homeless2009 = 'SELECT Year, Borough, "Homeless Estimates" FROM homeless_roster WHERE Year == 2009 GROUP BY Borough'
selected_Homeless2009 = psql.sqldf(homeless2009)
h2009data = pd.DataFrame(selected_Homeless2009)
print(h2009data)

homeless2010 = 'SELECT Year, Borough, "Homeless Estimates" FROM homeless_roster WHERE Year == 2010 GROUP BY Borough'
selected_Homeless2010 = psql.sqldf(homeless2010)
h2010data = pd.DataFrame(selected_Homeless2010)
print(h2010data)

homeless2011 = 'SELECT Year, Borough, "Homeless Estimates" FROM homeless_roster WHERE Year == 2011 GROUP BY Borough'
selected_Homeless2011 = psql.sqldf(homeless2011)
h2011data = pd.DataFrame(selected_Homeless2011)
print(h2011data)

homeless2012 = 'SELECT Year, Borough, "Homeless Estimates" FROM homeless_roster WHERE Year == 2012 GROUP BY Borough'
selected_Homeless2012 = psql.sqldf(homeless2012)
h2012data = pd.DataFrame(selected_Homeless2012)
print(h2012data)

#I then put this data into list, as this is what is needed for plotting to a bar graph. I customized the bars with its respective dataset, color and label to differentiate it from the others.
vals_2009 = list(h2009data['Homeless Estimates'])
bar1 = plt.bar(X_axis, vals_2009, width, color = 'lightblue', label = '2009')

vals_2010 = list(h2010data['Homeless Estimates'])
bar2 = plt.bar(X_axis+width, vals_2010, width, color = 'deepskyblue', label = '2010')

vals_2011 = list(h2011data['Homeless Estimates'])
bar3 = plt.bar(X_axis+width*2, vals_2011, width, color = 'turquoise', label = '2011')

vals_2012 = list(h2012data['Homeless Estimates'])
bar4 = plt.bar(X_axis+width*3, vals_2012, width, color = 'teal', label = '2012')

#This is the continuation of the styling of the graph. I labeled both the X and Y axes accordingly and titled it based on the data it was portraying.
plt.xlabel("Borough")
plt.ylabel("Homeless Estimates")
plt.title("Homeless Estimates Per Year By Borough (2009-2012)")

plt.xticks(X_axis + width, list(testing['Borough']))
plt.legend( (bar1, bar2, bar3, bar4), ('2009', '2010', '2011', '2012') )

#saves the size of the figure to the out file
plt.savefig('homelessEstimatesPerYearByBoroughGraph.png')
plt.show()

#Same approach is taken here for the scatter plot, but I get specific columns of the same length from different DataFrames, so that I am able to correlate the data and find a connection between them.
Xval = newDF2['numClinics']
Yval = newDF["Homeless Estimates"]

#This is used as the list of labels needed for the specific points in the scatter plot.
labelling=list(newDF2['Borough'])

#Method of creating the scatter plot
plt.figure(figsize=(8,6))
plt.scatter(Xval,Yval,s=500, alpha = 0.75, color="lightsteelblue")
plt.xlabel("Number Of Clinics")
plt.ylabel("Homeless Estimates")
plt.title("Correlation between Number of Clinics and Homeless Estimates in 2011",fontsize=15)
#how I put each label on its corresponding point on the graph
for i, label in enumerate(labelling):
    plt.annotate(label, (Xval[i], Yval[i]))

plt.savefig('homelessEstimatesAndNumClinics2011.png')
plt.show()

#The same exact thing as the previous scatter plot is done here as well, just with different data to show the correlation of those instead.
Xval_2 = allHomelessData['Homeless Estimates']
Yval_2 = newDF3['totalIndividuals']

labelling_2 = list(newDF3['Borough'])

plt.figure(figsize=(8,6))
plt.scatter(Xval_2,Yval_2,s=500, alpha = 0.75, color="purple")
plt.xlabel("Homeless Estimates")
plt.ylabel("Total Individuals in Shelter")
plt.title("Correlation between Homeless Estimates and Total Individuals in Shelter",fontsize=15)

for i, label in enumerate(labelling_2):
    plt.annotate(label, (Xval_2[i], Yval_2[i]))

plt.savefig('homelessEstimatesAndTotalIndividualsInShelter.png')
plt.show()


#This is the same method as before when I created the first bar graph.
X_axis_2 = np.arange(5)
width_2 = 0.20

#I brute-forced the data using queries and SQL to select all of the contents of the DataFrame newDF3 by the specified year 
shelter2018 = 'SELECT Year, Borough, totalIndividuals FROM newDF3 WHERE Year == 2018 GROUP BY Borough'
selected_Shelter2018 = psql.sqldf(shelter2018)
shel2018data = pd.DataFrame(selected_Shelter2018)
print(shel2018data)

shelter2019 = 'SELECT Year, Borough, totalIndividuals FROM newDF3 WHERE Year == 2019 GROUP BY Borough'
selected_Shelter2019 = psql.sqldf(shelter2019)
shel2019data = pd.DataFrame(selected_Shelter2019)
print(shel2019data)

shelter2020 = 'SELECT Year, Borough, totalIndividuals FROM newDF3 WHERE Year == 2020 GROUP BY Borough'
selected_Shelter2020 = psql.sqldf(shelter2020)
shel2020data = pd.DataFrame(selected_Shelter2020)
print(shel2020data)

shelter2021 = 'SELECT Year, Borough, totalIndividuals FROM newDF3 WHERE Year == 2021 GROUP BY Borough'
selected_Shelter2021 = psql.sqldf(shelter2021)
shel2021data = pd.DataFrame(selected_Shelter2021)
print(shel2021data)

#Each respective dataset gets its own bar, personalized with its color and label, which is the Year
vals_2018 = list(shel2018data['totalIndividuals'])
bar1_v2 = plt.bar(X_axis_2, vals_2018, width_2, color = 'slateblue', label = '2018')

vals_2019 = list(shel2019data['totalIndividuals'])
bar2_v2 = plt.bar(X_axis_2+width_2, vals_2019, width_2, color = 'darkslateblue', label = '2019')

vals_2020 = list(shel2020data['totalIndividuals'])
bar3_v2 = plt.bar(X_axis_2+width_2*2, vals_2020, width_2, color = 'mediumslateblue', label = '2020')

vals_2021 = list(shel2021data['totalIndividuals'])
bar4_v2 = plt.bar(X_axis_2+width_2*3, vals_2021, width_2, color = 'mediumpurple', label = '2021')

#Continued customization of the bar graph
plt.xlabel("Borough")
plt.ylabel("Total Individuals")
plt.title("Total Individuals in a Shelter Per Year By Borough (2018-2021)")

plt.xticks(X_axis_2 + width_2, list(testing['Borough']))
plt.legend( (bar1_v2, bar2_v2, bar3_v2, bar4_v2), ('2018', '2019', '2020', '2021') )

#saves the size of the figure to the out file
plt.savefig('totalIndividualsPerYearByBoroughGraph.png')
plt.show()