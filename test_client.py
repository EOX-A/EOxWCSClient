#!/usr/bin/env python


import sys
import os
import time

import wcs_client

input_params1={'request': 'GetCoverage','server_url': 'http://neso.cryoland.enveo.at/cryoland/ows?',  'coverageid': 'FSC_0.005deg_201404080650_201404081155_MOD_panEU_ENVEOV2.1.00.tif', 'subset_x': '28,30','subset_y': '59,61', 'format': 'jpeg'}
input_params2={'request': 'DescribeEOCoverageSet', 'server_url': 'http://neso.cryoland.enveo.at/cryoland/ows?' , 'eoID': 'daily_FSC_PanEuropean_Optical', 'subset_x' :'28,30', 'subset_y': '59,61' , 'subset_time':  '2012-03-17,2012-03-19T12:00:00Z' ,   'IDs_only':True}

elem=''
input_params3={'request': 'GetCoverage','server_url': 'http://neso.cryoland.enveo.at/cryoland/ows?', 'output':'/home/schillerc/cs_pylib/wcs_client/EOxWCSClient', 'coverageID': elem, 'subset_x' :'28,30', 'subset_y': '59,61', 'format': 'tiff' }

new = wcs_client.wcsClient()
result = new.DescribeEOCoverageSet(input_params2)

###
#   result=[u'FSC_0.005deg_201203170655_201203171155_MOD_panEU_ENVEOV2.1.00.tif', u'FSC_0.005deg_201203180730_201203181235_MOD_panEU_ENVEOV2.1.00.tif', u'FSC_0.005deg_201203190815_201203191145_MOD_panEU_ENVEOV2.1.00.tif']

for elem in result:
    print elem
    print 'ID',input_params3['coverageID']
    input_params3['coverageID']=elem
    print 'ID',input_params3['coverageID']
    new.GetCoverage(input_params3)






