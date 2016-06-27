# platform-get
Predicts train platforms

## Overview
````
Ingest pollers -> Data Store <-> Predictive analytics
                      |
                      V
                    Query
                   REST API
            Dude, where's my train?
````

## Setup
- python modules
  - suds
  - yaml
  - json
  - pymongo
  - ...
- Add your OpenLDBWS token to credentials.yml (tokens[darwin])
  - Register for your token [here](http://realtime.nationalrail.co.uk/OpenLDBWSRegistration/)

## Ingestion
poller that populates a database
- one poller per station
- get list of services (initially from a small set of CRS, inner london train stations)
- query service within a given range up to the point of departure (when it's departed, the service probably won't be updating with anything we care about)
- OR: use GetDepBoardWithDetails to get service details. Query this a lot, with the time offset 5 minutes in the past?

If ingest is stopped, should be able to catch up gradually

Ideally, should be able to find a service in the future, even if there isn't any data about it. Maybe have something that populates services on a less regular basis?

Suggest do the busiest railway stations
https://en.wikipedia.org/wiki/List_of_busiest_railway_stations_in_Great_Britain

Top 30:
- WAT London Waterloo
- VIC London Victoria
- LST London Liverpool Street
- LBG London Bridge
- CHX London Charing Cross
- EUS London Euston
- PAD London Paddington
- BHM Birmingham New Street
- KGX London King's Cross
- SRA Stratford
- GLC Glasgow Central
- LDS Leeds
- STP London St Pancras
- CLJ Clapham Junction
- MAN Manchester Piccadilly
- ECR East Croydon
- CST London Cannon Street
- VXH Vauxhall
- EDB Edinburgh Waverley
- HHY Highbury and Islington
- WIM Wimbledon
- FST London Fenchurch Street
- GTW Gatwick Airport
- BTN Brighton
- GLQ Glasgow Queen Street
- RDG Reading
- MYB London Marylebone
- LVC Liverpool Central
- BFR London Blackfriars
- LIV Liverpool Lime Street

Usage is capped at 5000/hr
If all 30, can update them every 30s at be at 3,600 req/hr

## Data Store
mongoDB? HBASE?

## Predictor
query mechanism that uses data and finds the likely platform

How should the platform be predicted?
Data inputs:
- platforms used for this service
- platforms used by this service at this time
- platforms used by this service on this day of the week
- platforms that are currently allocated

Maybe mapreduce jobs running, updating the platforms on a regular basis
Probably not driven by user queries

## REST API
- get departure boards/services filtered by station, time
- get information about this service
