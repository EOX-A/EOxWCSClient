#!/usr/bin/env python


import sys
import os
import time

import wcs_client




#======== Testing CryoLand

input_params1={'request': 'GetCoverage','server_url': 'http://neso.cryoland.enveo.at/cryoland/ows?',  'coverageid': 'FSC_0.005deg_201404080650_201404081155_MOD_panEU_ENVEOV2.1.00.tif', 'subset_x': '28,30','subset_y': '59,61', 'format': 'jpeg'}


input_params2={'request': 'DescribeEOCoverageSet', 'server_url': 'http://neso.cryoland.enveo.at/cryoland/ows?' , 'eoID': 'daily_FSC_PanEuropean_Optical', 'subset_lon' :'28,30', 'subset_lat': '59,61' , 'subset_time':  '2012-03-17,2012-03-19T12:00:00Z' ,   'IDs_only':True}

    ./cmdline_wcs_client.py DescribeEOCoverageSet -s 'http://neso.cryoland.enveo.at/cryoland/ows?' --eoID 'daily_FSC_PanEuropean_Optical' --subset_lon 28,30 --subset_lat 59,61 --subset_time 2012-03-17,2012-03-19T12:00:00Z --IDs_only 

## returned =>  (['FSC_0.005deg_201203170655_201203171155_MOD_panEU_ENVEOV2.1.00.tif', 'FSC_0.005deg_201203180730_201203181235_MOD_panEU_ENVEOV2.1.00.tif', 'FSC_0.005deg_201203190815_201203191145_MOD_panEU_ENVEOV2.1.00.tif'], ['lat', 'long'], '4326')


input_params3={'request': 'GetCoverage','server_url': 'http://neso.cryoland.enveo.at/cryoland/ows?', 'output':'/home/schillerc/cs_pylib/wcs_client/EOxWCSClient', 'coverageID': elem, 'subset_x' :'28,30', 'subset_y': '59,61', 'format': 'tiff' }





new = wcs_client.wcsClient()
result = new.DescribeEOCoverageSet(input_paramsD1a)

###
#   result=[u'FSC_0.005deg_201203170655_201203171155_MOD_panEU_ENVEOV2.1.00.tif', u'FSC_0.005deg_201203180730_201203181235_MOD_panEU_ENVEOV2.1.00.tif', u'FSC_0.005deg_201203190815_201203191145_MOD_panEU_ENVEOV2.1.00.tif']

elem=''
if len(result) > 0:
    for elem in result:
        print elem
        #print 'ID',input_params3['coverageID']
        input_paramsD1b['coverageID']=elem
        #print 'ID',input_params3['coverageID']
        new.GetCoverage(input_paramsD1b)
else:
    print 'No Coverages available'



#============== Testing DREAM 
### >>>  #---
### >>>   input_paramsD2a = dict(request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='', subset_x='', subset_y='',  subset_time='', IDs_only=True)
### >>>  ./wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID   --subset_lat   --subset_lon   --subset_time    --IDs_only

### >>>  #---
### >>>   elem=''
### >>>   input_paramsD2b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem,  subset_x='', subset_y='', format='tiff')
### >>>  ./wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows?  --coverageID   --subset_x    --subset_y   --format tiff


#http://data.eox.at/instance00/ows?  --EOID Landsat5_2A  -a 3.5,3.6,43.3,43.4    -t 20110513
    input_paramsD1a = dict( request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='Landsat5_2A', subset_lon='3.5,3.6', subset_lat='43.3,43.4', subset_time='2011-05-13,2011-06-13',  IDs_only=True)
    ./cmdline_wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID Landsat5_2A  --subset_lat 43.3,43.4  --subset_lon 3.5,3.6  --subset_time 2011-05-13,2011-06-13   --IDs_only

# returned =>    (['L930763_20110513_L5_197_030_USGS_surf_pente_30m', 'L930763_20110529_L5_197_030_USGS_surf_pente_30m'], ['x', 'y'], '2154')

#---
    elem=''
    input_paramsD1b = dict( request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem,  subset_x='epsg:4326 Long 3.5,3.6', subset_y='epsg:4326 Lat 43.3,43.4', format='tiff', output='/home/schillerc/tmp1/cryoland_tmp')
    ./cmdline_wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows? --coverageID  $elem   --subset_x epsg:4326 Long 3.5,3.6   --subset_y epsg:4326 Lat 43.3,43.4  --format tiff

#---
#http://data.eox.at/instance00/ows?  --EOID Landsat5_2A  -a 2,3,43,44    -t 20110520
    input_paramsD2a = dict(request='DescribeEOCoverageSet', server_url='', eoID='Landsat5_2A', subset_lat='43,44', subset_lon='2,3',  subset_time='011-05-20,2011-06-20', IDs_only=True)
    ./cmdline_wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID Landsat5_2A  --subset_lat 43,44   --subset_lon 2,3  --subset_time 2011-05-20,2011-06-20  --IDs_only

## (['L930663_20110520_L5_198_030_USGS_surf_pente_30m', 'L930663_20110529_L5_197_030_ESA_surf_pente_30m', 'L930663_20110614_L5_197_030_ESA_surf_pente_30m', 'L930664_20110520_L5_198_030_USGS_surf_pente_30m', 'L930664_20110529_L5_197_030_USGS_surf_pente_30m'], ['x', 'y'], '2154')

  
#---
    elem=''
    input_paramsD2b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem, subset_x='2,3', subset_y='43,44',  subset_time='', IDs_only=True)
    ./cmdline_wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows? --coverageID    --subset_x epsg:4326 Long 2,3 --subset_y epsg:4326 Lat 43,44   --format tiff
  
#
#Gulf of Lyon:
#http://data.eox.at/instance00/ows?  --EOID Spot4Take5_N2A_PENTE   -a 3.5,3.6,43.3,43.4     -t 20130227
    input_paramsD3a = dict(request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='Spot4Take5_N2A_PENTE', subset_lon='3.5,3.6', subset_lat='43.3,43.4',  subset_time='2013-02-27,2013-03-17', IDs_only=True)
    ./cmdline_wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID Spot4Take5_N2A_PENTE  --subset_lat 43.3,43.4  --subset_lon 3.5,3.6  --subset_time 2013-02-27,2013-03-17   --IDs_only

## (['SPOT4_HRVIR2_XS_20130227093758_N2A_PENTE', 'SPOT4_HRVIR2_XS_20130304093717_N2A_PENTE', 'SPOT4_HRVIR2_XS_20130314093636_N2A_PENTE'], ['x', 'y'], '2154')

  
#---
    elem=''
    input_paramsD3b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem, subset_x='3.5,3.6', subset_y='43.3,43.4',  subset_time='2013-02-27,2013-03-17', IDs_only=True)
    ./cmdline_wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows? --coverageID    --subset_x epsg:4326 Long 3.5,3.6  --subset_y epsg:4326 Lat 43.3,43.4   --format tiff

#
#Brussel:
#http://data.eox.at/instance00/ows?  --EOID Spot4Take5_N2A_PENTE   -a 4.76,5.10,50.52,50.78 -t 20130616
    input_paramsD4a = dict(request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='Spot4Take5_N2A_PENTE', subset_lon='4.76,5.10', subset_lat='50.52,50.78',  subset_time='2013-06-16,2013-07-01', IDs_only=True)
    ./cmdline_wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID Spot4Take5_N2A_PENTE  --subset_lat 50.52,50.78  --subset_lon 4.76,5.10  --subset_time 2013-06-16,2013-07-01   --IDs_only

## (['SPOT4_HRVIR1_XS_20130616094644_N2A_PENTE'], ['x', 'y'], '32631')
  
#---
    elem=''
    input_paramsD4b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem, subset_x='4.76,5.10', subset_y='50.52,50.78',  subset_time='2013-06-16,2013-07-01', IDs_only=True)
    ./cmdline_wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows? --coverageID   --subset_x epsg:4326 Long 4.76,5.10  --subset_y epsg:4326 Lat 50.52,50.78    --format tiff


#
#Bretagne
#http://data.eox.at/instance00/ows?  --EOID Spot4Take5_N2A_PENTE   -a -2.7,-2.6,47.6,47.7   -t 20130211 
    input_paramsD5a = dict(request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='Spot4Take5_N2A_PENTE', subset_lon='-2.7,-2.6', subset_lat='47.6,47.7',  subset_time='2013-02-11', IDs_only=True)
 ##   ./wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID  Spot4Take5_N2A_PENTE --subset_lat 47.6,47.7  --subset_lon -2.7,-2.6  --subset_time  2013-02-11  --IDs_only

## NEW ==>  cmdline_wcs_client.py / wcs_client.py
    ./cmdline_wcs_client.py  DescribeEOCoverageSet -s http://data.eox.at/instance00/ows?  --eoID  Spot4Take5_N2A_PENTE --subset_lat 47.6,47.7  --subset_lon -2.7,-2.6  --subset_time 2013-02-11  --IDs_only

## (['SPOT4_HRVIR1_XS_20130211095822_N2A_PENTE'], ['x', 'y'], '2154')


  
#---
  #SPOT4_HRVIR1_XS_20130211095822_N2A_PENTE
    elem=''
    input_paramsD5b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem, subset_x='-2.7,-2.6', subset_y='47.6,47.7',  subset_time='', IDs_only=True)
##    ./wcs_client.py  GetCoverage  -s http://data.eox.at/instance00/ows? --coverageID   --subset_x epsg:4326 Long -2.7,-2.6  --subset_y Lat epsg:4326  47.6,47.7   --format tiff  --output    --coverageID   
## NEW ==>  cmdline_wcs_client.py / wcs_client.py
./cmdline_wcs_client.py GetCoverage -s http://data.eox.at/instance00/ows?  --subset_x epsg:4326 Long -2.7,-2.6  --subset_y epsg:4326 Lat  47.6,47.7   --format tiff --output /home/schillerc/tmp1/cryoland_tmp --coverageID   




#
#

#
#http://data.eox.at/instance00/ows?  --EOID Landsat7_2A
#  input_paramsD3
#
#http://data.eox.at/instance00/ows?  --EOID Landsat_2A
#  input_paramsD4



#####################################################################################
####   for copy and paste into an ipython session --> use  %cpaste
#####################################################################################

## Attention -- use %cpaste !!!

import sys
import os
import time
import wcs_client

input_paramsD1a = dict( request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='Landsat5_2A', subset_lon='3.5,3.6', subset_lat='43.3,43.4', subset_time='2011-05-13,2011-06-13',  IDs_only=True)

elem=''
input_paramsD1b = dict( request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem,  subset_x='epsg:4326 Long 3.5,3.6', subset_y='epsg:4326 Lat 43.3,43.4', format='tiff', output='/home/schillerc/tmp1/cryoland_tmp', outputcrs='3035', size_x='100', size_y='150')


new = wcs_client.wcsClient()
result = new.DescribeEOCoverageSet(input_paramsD1a)
if len(result) > 0:
    for elem in result:
        print elem
        input_paramsD1b['coverageID']=elem
        new.GetCoverage(input_paramsD1b)
else:
    print 'No Coverages available'


del new

input_paramsD5a = dict(request='DescribeEOCoverageSet', server_url='http://data.eox.at/instance00/ows?', eoID='Spot4Take5_N2A_PENTE', subset_lon='-2.7,-2.6', subset_lat='47.6,47.7',  subset_time='2013-02-11', IDs_only=True)

elem=''
input_paramsD5b = dict(request='GetCoverage', server_url='http://data.eox.at/instance00/ows?', coverageID=elem, subset_x='epsg:4326 Long -2.7,-2.6', subset_y='epsg:4326 Lat 47.6,47.7', format='tiff', output='/home/schillerc/tmp1/cryoland_tmp')

new = wcs_client.wcsClient()
result = new.DescribeEOCoverageSet(input_paramsD5a)
if len(result) > 0:
    for elem in result:
        print elem
        input_paramsD5b['coverageID']=elem
        new.GetCoverage(input_paramsD5b)
else:
    print 'No Coverages available'







