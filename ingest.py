#!/usr/bin/env python

# see for examples:
# https://svn.fedorahosted.org/svn/suds/trunk/tests/rhq.py

import logging
import json
import yaml
import time
import datetime
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

while True:
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

        logging.info('Storing service ' +
                service.get('serviceID') + ' ' +
                service.get('std') + ' ' + ' ' +
                service.get('origin')['location'][0]['crs'] + ' -> ' +
                service.get('destination')['location'][0]['crs']
                )

        # TODO is serviceID guaranteed to be unique forever?
        servicesCollection.find_one_and_update(
            {'serviceID': service.get('serviceID')},
            {'$set':{
                'std': service.get('std'),
                'origin': service.get('origin'),
                'serviceType': service.get('serviceType'),
                'destination': service.get('destination'),
                'platform': service.get('platform'),
                'rsid': service.get('rsid'),
                'serviceID': service.get('serviceID'),
                'etd': service.get('etd'),
                'operator': service.get('operator'),
                'operatorCode': service.get('operatorCode'),
                'lastUpdated': datetime.datetime.utcnow().isoformat()
                }
            },
            upsert=True
        )

    time.sleep(30)
