#!/usr/bin/env python

# see for examples:
# https://svn.fedorahosted.org/svn/suds/trunk/tests/rhq.py

import yaml
import json
from suds.client import Client
from suds.sudsobject import asdict

def recursive_asdict(d):
  """Convert Suds object into serializable format."""
  out = {}
  for k, v in asdict(d).iteritems():
    if hasattr(v, '__keylist__'):
      out[k] = recursive_asdict(v)
    elif isinstance(v, list):
      out[k] = []
      for item in v:
        if hasattr(item, '__keylist__'):
          out[k].append(recursive_asdict(item))
        else:
          out[k].append(item)
    else:
      out[k] = v
  return out

def suds_to_json(data):
  return json.dumps(recursive_asdict(data))

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

#result = client.service.GetDepartureBoard(
result = client.service.GetDepBoardWithDetails(
  numRows,
  crs,
  filterCrs,
  filterType,
  timeOffset,
  timeWindow, )

# TODO guard against timeouts, request quota exceeded
print suds_to_json(result.trainServices)

# TODO serialize result to JSON
# TODO store result in mongodb
