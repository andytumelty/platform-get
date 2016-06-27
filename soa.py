#!/usr/bin/env python

# see for examples:
# https://svn.fedorahosted.org/svn/suds/trunk/tests/rhq.py

import yaml
from suds.client import Client

f = open('credentials.yml')
credentials = yaml.safe_load(f)
f.close()

url = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16'

client = Client(url)

token = client.factory.create('ns2:AccessToken')
token.TokenValue = credentials['tokens']['darwin']

client.set_options(soapheaders=token) 

# GetArrBoardWithDetails(xs:unsignedShort numRows, ns0:CRSType crs, ns0:CRSType filterCrs, ns0:FilterType filterType, xs:int timeOffset, xs:int timeWindow, )
# GetArrDepBoardWithDetails(xs:unsignedShort numRows, ns0:CRSType crs, ns0:CRSType filterCrs, ns0:FilterType filterType, xs:int timeOffset, xs:int timeWindow, )
# GetArrivalBoard(xs:unsignedShort numRows, ns0:CRSType crs, ns0:CRSType filterCrs, ns0:FilterType filterType, xs:int timeOffset, xs:int timeWindow, )
# GetArrivalDepartureBoard(xs:unsignedShort numRows, ns0:CRSType crs, ns0:CRSType filterCrs, ns0:FilterType filterType, xs:int timeOffset, xs:int timeWindow, )
# GetDepBoardWithDetails(xs:unsignedShort numRows, ns0:CRSType crs, ns0:CRSType filterCrs, ns0:FilterType filterType, xs:int timeOffset, xs:int timeWindow, )
# GetDepartureBoard(xs:unsignedShort numRows, ns0:CRSType crs, ns0:CRSType filterCrs, ns0:FilterType filterType, xs:int timeOffset, xs:int timeWindow, )
# GetFastestDepartures(ns0:CRSType crs, filterList filterList, xs:int timeOffset, xs:int timeWindow, )
# GetFastestDeparturesWithDetails(ns0:CRSType crs, filterList filterList, xs:int timeOffset, xs:int timeWindow, )
# GetNextDepartures(ns0:CRSType crs, filterList filterList, xs:int timeOffset, xs:int timeWindow, )
# GetNextDeparturesWithDetails(ns0:CRSType crs, filterList filterList, xs:int timeOffset, xs:int timeWindow, )
# GetServiceDetails(ns3:ServiceIDType serviceID, )
     
numRows = 10
crs = 'EUS'
filterCrs = None
filterType = None
timeOffset = 10
timeWindow = 10

result = client.service.GetDepartureBoard(
  numRows,
  crs,
  filterCrs,
  filterType,
  timeOffset,
  timeWindow, )

print result
