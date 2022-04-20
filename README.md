# PlaNET: Blueprinting the Future of Transport

PlaNET is an application designed for city planners to better understand and improve their transportation systems.

## Inspiration

Public transport is the foundation of human mobility in a modern society. Building an effective public transport system is pivotal to promoting a car-lite society. Often, urban areas are subjected to convoluted public transport networks, swaying commuters towards personal vehicles as their preferred mode of transport. Apart from the environmental impacts of shifting away from individual vehicles, it relieves traffic congestion. Public transport systems consist of various intricate mechanisms and factors, which poses a challenge when planning and implementing an effective transport system that brings large volumes of commuters from one location to another. Furthermore, developing effective public transport infrastructure requires a deep understanding of qualitative factors, such as commuter preferences and behaviours. 

This work aims to alleviate challenges city planners face when organising the multitudes of moving components by leveraging graph database and graph analytics to uncover insights on how the public transport network is serving commuters in their journeys. From there, gaps and opportunities to optimise efficiency of public transport services can be identified to improve journeys.

## What it does

PlaNET is a project done using TigerGraph which aims to aid city planners in building effective public transportation systems by better understanding commuter behaviour. It helps to visualise and understand how the public transport network serves commuter journeys and identify gaps and opportunities to optimise efficiency of public transport services to cater to commuter travel preferences. Streamlit is used as a reporting tool to help understand the graph network. 

## How we built it

At its core, PlaNET queries from a TigerGraph database, traversing the graph and calculating metrics. With the help of GraphStudio, queries are written, debugged, tested and installed to the graph. Streamlit is used as a frontend framework to visualise the results, uncovering insights.

### Database Schema

![](./images/Schema.png)

### Datasets

In order to analyse the public transport system on its effectiveness, real world datasets need to be collected and loaded into the database. The datasets need to be detailed enough in order to be informative. The following datasets are chosen for the scope of this project:

- Bus Services
- Bus Stops
- Subway/Train Services
- Subway/Train Stations
- Trips, with Origin and Destination Stops/Stations

It is challenging to obtain a stuctured form of these data for a particular city as they are not readily available in a tabular format. Upon research, New York City (NYC) was identified to be an urban location that have the aforementioned datasets.

#### Bus Routes and Bus Stops

The bus stop dataset is obtained from Miranda Adams's [NYC-bus-stops-by-route Github page](https://github.com/miranda-adams/NYC-bus-stops-by-route). The bus routes dataset is obtained from the [Metropolitan Transportation Authority (MTA) website](https://bustime.mta.info/m).

#### Subway Routes and Subway Stations

Subway datasets are retrieved from the New York City Transit Subway data from [MTA's developer website](http://web.mta.info/developers/developer-data-terms.html#data).

#### Origin-Destination Data (Proxy for Trips)

For trips, the fare card data by the State of New York for MTA is considered, but it has a few limitations:

- Data is aggregated weekly
- Exit stations (where commuters leave the subway) are not recorded
- Bus data is not included

Thus, another dataset that is more rich should be used. Since there is no trip level dataset for public transport, the [New York City Taxi Trip Duration](https://www.kaggle.com/competitions/nyc-taxi-trip-duration/data) dataset is used. In this dataset, the coordinates (latitude and longitude) for both origin and destination are available. Coupled with the Google Maps Directions API (elaborated in the following section), this dataset for taxi trips can be a proxy to represent public transport trips.

### Data Processing and Loading

#### Bus Routes and Bus Stops

The bus stop dataset is obtained from Miranda Adams's [NYC-bus-stops-by-route Github page](https://github.com/miranda-adams/NYC-bus-stops-by-route), which provides a dataset with the bus stop names, their IDs as well as their latitudes and longitudes. This bus routes dataset is used to load the vertex `BusStation`.

The bus routes dataset is obtained from the [Metropolitan Transportation Authority (MTA) website](https://bustime.mta.info/m), where the mobile version of their Bus Time page lists all their bus services. Searching for a bus service lists all the bus stops, their IDs and their sequences. This data is joined with the data from the Github page to get the latitude and longitude for each bus stop. This bus routes dataset is used to load the edge `serve` from `BusService` to `BusStation`.

The bus routes dataset is then used to derive the bus service dataset, which contains the unique bus services along with the directions that the buses operates in. This bus service dataset is used to load the vertex `BusService`.

#### Subway Routes and Subway Stations

The subway route dataset is derived from the stop times and stops datasets from MTA's developer website. From the stop times, the route and direction were identified to be in the trip id and stop id respectively, which is sufficient for `TrainService`. Each route and direction are then aggregated and the longest sequence (stop sequence) of station stops is identified. This subway route dataset is crucial in loading the edges `serve` from `TrainService` to `TrainStation` too.

As for the subway stations dataset, the stops dataset is joined with the stop times to filter for stations that are in at least a route. This dataset is then used to load `TrainStation`.

#### Trips

The origin and destination coordinates from taxi trips sampled on a range of 5 days are extracted. To retrieve the travel mode (to public transport), the [Python client for Google Maps Directions API](https://github.com/googlemaps/google-maps-services-python) is used. The departure times for taxis are used when generating the public transport routes.

The first route for each trip is extracted from the Directions API response. Each route is broken down into multiple directions legs, where details of how to get from one location to another is detailed.

For instance, a route from the Empire State Building to Central Park starts from walking to 34 St - Herald Sq station, then taking the F Line (subway) to 57 Street station, then walking to Central Park. This route consists of 3 legs (walk, subway, walk) and modelled as 4 `waypoint` (Empire State Building, 34 St - Herald Sq station, 57 Street station, Central Park) and `utilise` 1 public transport (subway) service (F Line (subway) from 34 St - Herald Sq station to 57 Street station).

After processing each trip, the transit directions legs are then mapped with `BusService`, `BusStop`, `TrainService` and `TrainStation`.

## Insights

![](./images/Trains.png)
![](./images/Bus.png)

From the bar charts above, we observe that bus service M15 and train line 1 are the most frequently used services with the highest degree centrality score of 916 and 2394 respectively. This indicates that the service nodes are the most connected with our dataset of commuter journeys.

Similarly, bus stop 551131 and the Times Sq -42 St train station is the most strategically located and connected bus stop and train station based on commuter behaviour with the highest degree centrality score of 427 and 630 respectively. 

This signals to city planners that these stations and services are pivotal to the public transport system based on commuter demand. Rerouting services away from these stops might result in a dip in public transport utilisation.

Drilling down into bus service M15, we can explore commuter behaviours with the bus network analysis page of PlaNET’s streamlit reporting tool.

![](./images/Bus_Network_Analysis.png)

Looking at the histogram of departure times, we observe a huge spike in the number of journeys that depart at roughly 8am in the morning. 

The graph dips back down and stabilises for the hours approximately between 12pm to 6pm before gradually picking up again, corresponding to typical working hours. 

The spike after 6pm is much more gradual compared to the morning rush hour, indicating that departure times for commuters back home are more spread out across different hours in the evening. 

City planners can utilise this to adjust the deployment frequency of bus service to match the demand for each service.

Navigating to the train network analysis page, we can explore line 1.

![](./images/Train_Network_Analysis.png)

A total of 2287 trips utilise train line 1 which operates across 38 stations, with the average travel time being around 21 mins. The map above illustrates that the departure point of the trips, represented by the purple points, are clustered nearer to the city. 

City planners can identify potential locations for new train stations to add to train lines based on clustering starting location of trips.


## Challenges we ran into

Using and learning about graph databases meant that our team had to think of storing data from a different perspective than traditional databases. Most of us were new to graph databases and having the TigerGraph 101 tutorial helped us to familiarise ourselves not only with TigerGraph’s platform, but also provided an overview of graph databases to get us started on our project. 

Despite this, we still faced an uphill battle trying to define a schema for and mapping transportation systems to public transport utilisation trips data as there were multiple relationships and variables to consider. For example, while loading data into the graph database, we encountered problems such as graph databases defaulting to upsert when inserting data that has the same source and target. This made us rethink and recreate our schema from scratch to accommodate this behaviour. 

We also faced issues where there were syntax inconsistencies and compatibility issues between the new syntax and the current version of GraphStudio which encumbered our progress in schema creation and querying. Lastly, documentation and third-party resources are sparse.

## Accomplishments that we're proud of

We are proud that we managed to create our own graph database schema in TigerGraph, and load the data into the graph database successfully. It was a challenging experience when developing the relevant GSQL queries. Apart from TigerGraph, we learnt how to utilise external APIs to enrich our data - using Google Maps Directions API to structure public transport trips.

## What we learned

We learnt much more about TigerGraph as a platform, constructing GSQL, the Python client for Google Maps Directions API. Finally, we also learnt more about New York City!

## What's next for PlaNET

  - Utilise GNN to model and simulate trips to better understand and interpret consumer trip preferences
  - Perform geospatial analysis on the transport network
  - Getting actual public transport trips data to analyse 


## Devpost Link


## GitHub Link

