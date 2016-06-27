#!/usr/bin/env python

# see for examples:
# https://svn.fedorahosted.org/svn/suds/trunk/tests/rhq.py

import yaml
from suds.client import Client

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

print result

# TODO serialize result to JSON
# TODO store result in mongodb
