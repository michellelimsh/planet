# PlaNET

PlaNET is an application designed for city planners to better understand and improve their transportation systems


## Inspiration

- Deliver transport insights to diagnose and validate assumptions to plan and develop an efficient public transport network

- Analysis to identify gaps and opportunities within their public transport network

- Understanding commuter transport preferencesd usage of public transport services

- Visualise and understand how the public transport network serves commuter journeys and identify gaps and opportunities to optimise efficiency of public transport services to commuter travel preferences

## Problem Statement: Develop Effective Public Transportation System

## Database Schema

## Datasets

In order to analyse the public transport system on its effectiveness, real world datasets need to be collected and loaded into the database. The datasets need to be detailed enough in order to be informative. The following datasets are chosen for the scope of this project:

- Bus Services
- Bus Stops
- Subway/Train Services
- Subway/Train Stations
- Trip Level Fare Card Data, with Origin and Destination Stops/Stations

It is challenging to obtain a stuctured form of these data for a particular city as they are not readily available in a tabular format. Upon research, New York City (NYC) was identified to be an urban location that have the aforementioned datasets.

###  Bus Routes and Bus Stops

The bus routes dataset is obtained from the [Metropolitan Transportation Authority (MTA) website](https://bustime.mta.info/m), where the mobile version of their Bus Time page lists all their bus services. Searching for a bus service lists all the bus stops and their sequences.

### Subway Routes and Subway Stations

Subway datasets are retrieved from the New York City Transit Subway data from [MTA's developer website](http://web.mta.info/developers/developer-data-terms.html#data).

### Origin-Destination Data (Proxy for Fare Card Data)

The fare card data by the State of New York for MTA has a few limitations:

- Data is aggregated weekly
- Exit stations (where commuters leave the subway) are not recorded
- Bus data is not included

Thus, another dataset that is more rich should be used. Since there is no trip level dataset for public transport, the [New York City Taxi Trip Duration](https://www.kaggle.com/competitions/nyc-taxi-trip-duration/data) dataset is used. In this dataset, the coordinates (latitude and longitude) for both origin and destination are available. Coupled with the Google Maps Directions API (which will be elaborated in the following section), this dataset for taxi trips can be a proxy to represent public transport trips.

## Data Processing and Loading


## Acknowledgements
