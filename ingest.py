#!/usr/bin/env python

# see for examples:
# https://svn.fedorahosted.org/svn/suds/trunk/tests/rhq.py

import logging
import json
import yaml
from suds.client import Client
from suds.sudsobject import asdict
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

def recursive_asdict(data):
    """Convert Suds object into serializable format."""
    out = {}
    for key, val in asdict(data).iteritems():
        if hasattr(val, '__keylist__'):
            out[key] = recursive_asdict(val)
        elif isinstance(val, list):
            out[key] = []
            for item in val:
                if hasattr(item, '__keylist__'):
                    out[key].append(recursive_asdict(item))
                else:
                    out[key].append(item)
        else:
            out[key] = val
    return out

def suds_to_json(data):
    """Convert Suds object into JSON format."""
    return json.dumps(recursive_asdict(data))

logging.info('Loading credentials')

# TODO bomb out if can't read necessary credentials
# TODO optionally use ENV variables for tokens
f = open('credentials.yml')
credentials = yaml.safe_load(f)
f.close()

url = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16'

client = Client(url)

token = client.factory.create('ns2:AccessToken')
token.TokenValue = credentials['tokens']['darwin']

client.set_options(soapheaders=token) 

# TODO check token credentials
         
numRows = 10
crs = 'EUS'
filterCrs = None
filterType = None
timeOffset = -5
timeWindow = 120

# TODO split into poller objects, create one per CRS
# TODO define CRS in a config file somewhere

logging.info('Getting data')
#result = client.service.GetDepartureBoard(
result = client.service.GetDepBoardWithDetails(
    numRows,
    crs,
    filterCrs,
    filterType,
    timeOffset,
    timeWindow, )

# TODO guard against timeouts, request quota exceeded
services = recursive_asdict(result.trainServices)

dbName = 'platform_get'
dbHost = 'localhost'
dbPort = 27017

# TODO change to use db config from file
dbClient = MongoClient(dbHost, dbPort)
db = dbClient[dbName]
servicesCollection = db.services

# insert or update
for service in services['service']:
    # print service
    print service.get('std')
    print service.get('origin')
    print service.get('serviceType')
    print service.get('destination')
    print service.get('platform')
    print service.get('rsid')
    print service.get('serviceID')
    print service.get('etd')
    print service.get('operator')
    print service.get('operatorCode')
