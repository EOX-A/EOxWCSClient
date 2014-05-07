#!/usr/bin/env python


import sys
import os
import time

import wcs_client




#======== Testing CryoLand

input_params1={'request': 'GetCoverage','server_url': 'http://neso.cryoland.enveo.at/cryoland/ows?',  'coverageid': 'FSC_0.005deg_201404080650_201404081155_MOD_panEU_ENVEOV2.1.00.tif', 'subset_x': '28,30','subset_y': '59,61', 'format': 'jpeg'}
input_params2={'request': 'DescribeEOCoverageSet', 'server_url': 'http://neso.cryoland.enveo.at/cryoland/ows?' , 'eoID': 'daily_FSC_PanEuropean_Optical', 'subset_lon' :'28,30', 'subset_lat': '59,61' , 'subset_time':  '2012-03-17,2012-03-19T12:00:00Z' ,   'IDs_only':True}

input_params3={'request': 'GetCoverage','server_url': 'http://neso.cryoland.enveo.at/cryoland/ows?', 'output':'/home/schillerc/cs_pylib/wcs_client/EOxWCSClient', 'coverageID': elem, 'subset_x' :'28,30', 'subset_y': '59,61', 'format': 'tiff' }


new = wcs_client.wcsClient()
result = new.DescribeEOCoverageSet(input_params2)

###
#   result=[u'FSC_0.005deg_201203170655_201203171155_MOD_panEU_ENVEOV2.1.00.tif', u'FSC_0.005deg_201203180730_201203181235_MOD_panEU_ENVEOV2.1.00.tif', u'FSC_0.005deg_201203190815_201203191145_MOD_panEU_ENVEOV2.1.00.tif']

elem=''
for elem in result:
    print elem
    #print 'ID',input_params3['coverageID']
    input_params3['coverageID']=elem
    #print 'ID',input_params3['coverageID']
    new.GetCoverage(input_params3)



#============== Testing DREAM 
### >>>  #---
### >>>   input_paramsD2a = dict(request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='', subset_x='', subset_y='',  subset_time='', IDs_only=True)
### >>>  ./wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID   --subset_lat   --subset_lon   --subset_time    --IDs_only

### >>>  #---
### >>>   elem=''
### >>>   input_paramsD2b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem,  subset_x='', subset_y='', format='tiff')
### >>>  ./wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows?  --coverageID   --subset_x    --subset_y   --format tiff


#http://data.eox.at/instance00/ows?  --EOID Landsat5_2A  -a 3.5,3.6,43.3,43.4    -t 20110513
    input_paramsD1a = dict( request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='Landsat5_2A', subset_x='3.5,3.6', subset_y='43.3,43.4', subset_time='2011-05-13,2011-06-13',  IDs_only=True)
    ./wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID Landsat5_2A  --subset_lat 43.3,43.4  --subset_lon 3.5,3.6  --subset_time 2011-05-13,2011-06-13   --IDs_only

# returned CoverageIds =>    [u'L930763_20110513_L5_197_030_USGS_surf_pente_30m', u'L930763_20110529_L5_197_030_USGS_surf_pente_30m']

#---
    elem=''
    input_paramsD1b = dict( request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem,  subset_x='3.5,3.6', subset_y='43.3,43.4', format='tiff')
    ./wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows? --coverageID     --subset_x 3.5,3.6   --subset_y 43.3,43.4  --format tiff

#---
#http://data.eox.at/instance00/ows?  --EOID Landsat5_2A  -a 2,3,43,44    -t 20110520
    input_paramsD2a = dict(request='DescribeEOCoverageSet', server_url='', eoID='Landsat5_2A', subset_x='43,44', subset_y='2,3',  subset_time='011-05-20,2011-06-20', IDs_only=True)
    ./wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID Landsat5_2A  --subset_lat 43,44   --subset_lon 2,3  --subset_time 2011-05-20,2011-06-20  --IDs_only
  
#---
    elem=''
    input_paramsD2b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem, subset_x='2,3', subset_y='43,44',  subset_time='', IDs_only=True)
    ./wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows? --coverageID    --subset_x  2,3 --subset_y 43,44   --format tiff
  
#
#Gulf of Lyon:
#http://data.eox.at/instance00/ows?  --EOID Spot4Take5_N2A_PENTE   -a 3.5,3.6,43.3,43.4     -t 20130227
    input_paramsD3a = dict(request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='Spot4Take5_N2A_PENTE', subset_x='3.5,3.6', subset_y='43.3,43.4',  subset_time='2013-02-27,2013-03-17', IDs_only=True)
    ./wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID Spot4Take5_N2A_PENTE  --subset_lat 43.3,43.4  --subset_lon 3.5,3.6  --subset_time 2013-02-27,2013-03-17   --IDs_only
  
#---
    elem=''
    input_paramsD3b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem, subset_x='3.5,3.6', subset_y='43.3,43.4',  subset_time='2013-02-27,2013-03-17', IDs_only=True)
    ./wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows? --coverageID    --subset_x 3.5,3.6  --subset_y 43.3,43.4   --format tiff

#
#Brussel:
#http://data.eox.at/instance00/ows?  --EOID Spot4Take5_N2A_PENTE   -a 4.76,5.10,50.52,50.78 -t 20130616
    input_paramsD4a = dict(request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='Spot4Take5_N2A_PENTE', subset_x='4.76,5.10', subset_y='50.52,50.78',  subset_time='2013-06-16,2013-07-01', IDs_only=True)
    ./wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID Spot4Take5_N2A_PENTE  --subset_lat 50.52,50.78  --subset_lon 4.76,5.10  --subset_time 2013-06-16,2013-07-01   --IDs_only
  
#---
    elem=''
    input_paramsD4b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem, subset_x='4.76,5.10', subset_y='50.52,50.78',  subset_time='2013-06-16,2013-07-01', IDs_only=True)
    ./wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows? --coverageID   --subset_x 4.76,5.10  --subset_y  50.52,50.78    --format tiff

#
#Bretagne
#http://data.eox.at/instance00/ows?  --EOID Spot4Take5_N2A_PENTE   -a -2.7,-2.6,47.6,47.7   -t 20130211 
    input_paramsD5a = dict(request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='Spot4Take5_N2A_PENTE', subset_x='-2.7,-2.6', subset_y='47.6,47.7',  subset_time='20130211', IDs_only=True)
    ./wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID  Spot4Take5_N2A_PENTE --subset_lat 47.6,47.7  --subset_lon -2.7,-2.6  --subset_time  20130211  --IDs_only
  
#---
    elem=''
    input_paramsD5b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem, subset_x='2.7,-2.6', subset_y='47.6,47.7',  subset_time='', IDs_only=True)
    ./wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows? --coverageID   --subset_x 2.7,-2.6  --subset_y 47.6,47.7   --format tiff

#
#

#
#http://data.eox.at/instance00/ows?  --EOID Landsat7_2A
#  input_paramsD3
#
#http://data.eox.at/instance00/ows?  --EOID Landsat_2A
#  input_paramsD4







