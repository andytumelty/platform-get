#!/usr/bin/env python

# see for examples:
# https://svn.fedorahosted.org/svn/suds/trunk/tests/rhq.py

import logging
import json
import yaml
import time
import datetime
import thread
import ConfigParser
from suds.client import Client
from suds.sudsobject import asdict
from pymongo import MongoClient

# FIXME what if ingest.cfg doesn't exist? doesn't contain what is needed?
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read('ingest.cfg')

crsList     = config.get('suds','crsList').split(',')
numRows     = config.get('suds','numRows')
filterCrs   = config.get('suds','filterCrs')
filterType  = config.get('suds','filterType')
timeOffset  = config.get('suds','timeOffset')
timeWindow  = config.get('suds','timeWindow')

logging.basicConfig(
        filename='ingest.log',
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S%Z',
        level=logging.INFO)
logging.Formatter.converter = time.gmtime

logging.info('Starting platform-get ingest.py')

dbName = 'platform_get'
dbHost = 'localhost'
dbPort = 27017

# TODO change to use db config from file
dbClient = MongoClient(dbHost, dbPort)
db = dbClient[dbName]
servicesCollection = db.services

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

# FIXME ? should this be a class instead of a method?
def poller(crs):
    """ingestion polling for a station"""

    logging.info('Starting poller for ' + crs)
    while 1:
        logging.info('Getting data for ' + crs)

        # TODO guard against timeouts, request quota exceeded
        result = client.service.GetDepBoardWithDetails(
            numRows,
            crs,
            filterCrs,
            filterType,
            timeOffset,
            timeWindow, )

        services = recursive_asdict(result.trainServices)

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
                { 'serviceID': service.get('serviceID') },
                { '$set': {
                    'std':          service.get('std'),
                    'origin':       service.get('origin'),
                    'serviceType':  service.get('serviceType'),
                    'destination':  service.get('destination'),
                    'platform':     service.get('platform'),
                    'rsid':         service.get('rsid'),
                    'serviceID':    service.get('serviceID'),
                    'etd':          service.get('etd'),
                    'operator':     service.get('operator'),
                    'operatorCode': service.get('operatorCode'),
                    'lastUpdated':  datetime.datetime.utcnow().isoformat()
                    }
                },
                upsert=True
            )

        time.sleep(30)

url = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16'

client = Client(url)

# TODO bomb out if can't read necessary credentials
# TODO optionally use ENV variables for tokens
# TODO check token credentials
token = client.factory.create('ns2:AccessToken')
token.TokenValue = config.get('tokens','darwin')
client.set_options(soapheaders = token) 

try:
    for crs in crsList:
        thread.start_new_thread(poller, (crs,))
        # Keeps the logging nice, and evens out requests
        time.sleep(1)
except:
    logging.error('Unable to start thread')

while 1:
    pass
