#!/usr/bin/env python

##TODO - finish description

#------------------------------------------------------------------------------
#
#
#       General purpose WCS Client
#         - GetCapabilities Request
#         - DescribeCoverage Request
#         - DescribeEOCoverageSet Request
#         - GetMap Request
#
#         - return responses 
#         - reformat and list responses
#         - download coverages
#         - download time-series of coverages
#         - 
#         - allow user to specify:
#           + Area of Interest (subset)
#           + Time of Interest
#           + DatasetSeries or Coverage
#           + Server
#           + Rangesubsetting (eg. Bands)
#           + File-Format for downloads
#           + CRS for downloads
#           + Data-Type for downloads
#           + Mediatype
#           + 
## TODO: 
##  #           + updateSequence
##  #           + containment
##  #           + section
##  #           + count
##  #           + interpolation
##  #           + size or resolution
##  #           + mask
##  #           + 
#
#
#
# Name:        wcs_client.py
# Project:     DeltaDREAM
# Author(s):   Christian Schiller <christian dot schiller at eox dot at>
##
#-------------------------------------------------------------------------------
# Copyright (C) 2014 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------
#
#
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------


import sys
import os
import time
import argparse
#import tempfile
import shutil
import urllib2,  socket
from xml.dom import minidom

global __version__
__version__ = '0.1-beta'

    # check for OS Platform and set the Directory-Separator to be used
global dsep
dsep = os.sep

global temp_storage
temp_storage = None
try_dir=['TMP','TEMP','HOME','USER']
for elem in try_dir:
    temp_storage=os.getenv(elem)
    if temp_storage != None:
        break
    
if temp_storage is None:
    cur_dir = os.getcwd()
    temp_storage = cur_dir+'/tmp'




#/************************************************************************/
#/************************************************************************/
def test_print(input_params):
    # for testing @@@
#----
    print "I'm in "+sys._getframe().f_code.co_name
    
    print 
    for param, arg in input_params.items():
        if arg == None:
            print param+': --'
        else:
            print param+': ', arg


#/************************************************************************/
#/*                            do_interupt()                                     */
#/************************************************************************/
def do_interupt():
    """
        stop at call, to allow interactive usage with eg. IPython
        and variable exploration for dubugging
    """
    print "I'm in "+sys._getframe().f_code.co_name
    
    import pdb              # @@
    pdb.set_trace() 
    print 'stop here' 

#/************************************************************************/
#/*                            now()                                     */
#/************************************************************************/
def now():
    """
        get the current time stamp eg. for error messages
    """
    print "I'm in "+sys._getframe().f_code.co_name
    
    return  time.strftime('[%Y%m%dT%H%M%S] - ')


#/************************************************************************/
#/*                               handle_error()                              */
#/************************************************************************/


def handle_error(err_msg, err_code):
    """
        prints out the error_msg and err_code and exit
        Mainly used during debugging
    """
    print "I'm in "+sys._getframe().f_code.co_name    
    
    print err_msg, '; Error_Code =', err_code
#    usage()
    sys.exit(err_code)


#/************************************************************************/
#/*                              do_cleanup()                            */
#/************************************************************************/
def do_cleanup_tmp(temp_storage, cf_result, input_params):
    """
        clean up the temporary storagespace  used during download and processing
    """
    print "I'm in "+sys._getframe().f_code.co_name
    
    for elem in cf_result:
        shutil.copy2(temp_storage+dsep+elem, input_params['output_dir'])

    if os.path.exists(input_params['output_dir']+cf_result[0]) \
      and os.path.exists(input_params['output_dir']+cf_result[1]) \
      and os.path.exists(input_params['output_dir']+cf_result[2]):
          # remove all the temporay storage area
#        shutil.rmtree(temp_storage, ignore_errors=True)
        print '[Info] -- The Cloud-free dataset has been generated and is available at: '
        for elem in cf_result:
            print '  - ', input_params['output_dir']+elem
    else:
        print '[Error] -- The generated output-file could not be written to: ', input_params['output_dir']+cf_result
        sys.exit(7)


#/************************************************************************/
#/*                           do_print_flist()                           */
#/************************************************************************/
def do_print_flist(name, a_list):
    f_cnt = 1
#    print name, len(list), type(list)
    for elem in a_list:
        print  name, f_cnt,': ', elem
        f_cnt += 1


#/************************************************************************/
#/*                           do_print_flist()                           */
#/************************************************************************/

def validate_date(indate):
    """
        validate the input date and date format
    """
    print "I'm in "+sys._getframe().f_code.co_name
    
    try:
        parsed = time.strptime(indate, "%Y-%m-%d")

    except ValueError as e:
        err_code = 101
        err_msg = "[Error] - Wrong input date format OR invalid date (Format should be: 2013-05-08) => {0}".format(e)
        handle_error(err_msg, err_code)

    else:
        return parsed[:3]
 
#/************************************************************************/
#/*                           ()                           */
#/************************************************************************/







#/************************************************************************/
#/************************************************************************/
#/*                              wcsClient()                             */
#/************************************************************************/

class wcsClient(object):
    """
        WCS client for WCS 2.0/EO-WCS server access
    """
        # default timeout for all sockets (in case a requests hangs)
    timeout = 180
    socket.setdefaulttimeout(timeout)

        # XML search tags for the request responses
    xml_ID_tag = ['wcseo:DatasetSeriesId', 'wcs:CoverageId' ]
    xml_date_tag = ['gml:beginPosition',  'gml:endPosition']


    
    def __init__(self):
        pass


    #/************************************************************************/
    #/*                             set_base_request()                           */
    #/************************************************************************/
    def set_base_request(self):
        """
            sets the basic url components for a request
        """
        print "I'm in "+sys._getframe().f_code.co_name
        
        base_request = {'service': 'service=wcs',
                'version': '&version=2.0.1'}
        
       
        return base_request

    #/************************************************************************/
    #/*                             set_base_cap()                           */
    #/************************************************************************/
    def set_base_cap(self):
        """
            sets the basic url components for a GetCapabilities
            request
        """
        print "I'm in "+sys._getframe().f_code.co_name

        base_cap = {'request': '&request=', 
            'server_url': '' ,
            'updateSequence': '&updateSequence=', 
            'sections' :'&sections=' }
        
        
        return base_cap


    #/************************************************************************/
    #/*                             set_base_desccov()                       */
    #/************************************************************************/
    
    def set_base_desccov(self):
        """
            sets the basic urls components for a DescribeCoverage Request
            Input:  eoid
        """
        print "I'm in "+sys._getframe().f_code.co_name
        
        base_desccov = {'request': '&request=',
            'server_url': '' ,
            'coverageID': '&coverageID=' }
    
        return base_desccov
    
    
    #/************************************************************************/
    #/*                             set_set_base_desceocovset()              */
    #/************************************************************************/
    
    def set_base_desceocoverageset(self):
        """
            sets the basic urls components for a DescribeEOCoverageSet Request
            Allowd Values:  
        """
        print "I'm in "+sys._getframe().f_code.co_name
        
        set_base_desceocoverageset= {'request': '&request=',
            'server_url': '' ,
            'eoID': '&eoID=' ,
            'subset_x': '&subset=x,http://www.opengis.net/def/crs/EPSG/0/4326(' ,
            'subset_y': '&subset=y,http://www.opengis.net/def/crs/EPSG/0/4326(' ,
            'subset_time': '&subset=phenomenonTime(%22',
            'containment': '&containment=',
            'section': '&section=', 
            'count': '&count=',
            'IDs_only': False}

    
        return set_base_desceocoverageset
    
    
    
    #/************************************************************************/
    #/*                             set_base_getcov()                        */
    #/************************************************************************/
    def set_base_getcov(self):
        """
            sets the basic urls components for a GetCoverage Request
            Allowd Values: 
        """
        print "I'm in "+sys._getframe().f_code.co_name
        
        getcov_dict = {'request': '&request=', 
            'server_url': ''    , 
            'coverageID': '&coverageid=',  
            'format': '&format=image/',  
            'subset_x': '&subset=x,http://www.opengis.net/def/crs/EPSG/0/4326(',
            'subset_y': '&subset=y,http://www.opengis.net/def/crs/EPSG/0/4326(',  
            'rangesubset': '&rangesubset=', 
            'outputcrs': '&output_crs=epsg:' ,
            'interpolation': '&interpolation=',
            'mediatype': '&mediatype=',
            'mask': '&polygon,http://www.opengis.net/def/crs/EPSG/0/4326(',
            'size_x': '&size=x(' ,
            'size_y': '&size=y(' ,
            'output': None }


        return getcov_dict
    
    
    #/************************************************************************/
    #/*                           GetCapabilities()                          */
    #/************************************************************************/
    
    
    def GetCapabilities(self, input_params):
        """
            
        """
        print "I'm in "+sys._getframe().f_code.co_name
        
        procedure_dict = self.set_base_cap()
        http_request = self.create_request(input_params, procedure_dict)

        #test_print(input_params)
        
        return http_request
 
   
    #/************************************************************************/
    #/*                           DescribeCoverage()                         */
    #/************************************************************************/
    
    def DescribeCoverage(self, input_params):
        """
            
        """
        print "I'm in "+sys._getframe().f_code.co_name
        
        procedure_dict = self.set_base_desccov()
        
        http_request = self.create_request(input_params, procedure_dict)
        result_xml = wcsClient.execute_xml_request(self, http_request)

        return result_xml 

    
    #/************************************************************************/
    #/*                          DescribeEOCoverageSet()                     */
    #/************************************************************************/
    def DescribeEOCoverageSet(self, input_params):
        """
            
        """
        print "I'm in "+sys._getframe().f_code.co_name
        
        procedure_dict = self.set_base_desceocoverageset()
        http_request = self.create_request(input_params, procedure_dict)

        if input_params.has_key('IDs_only') and input_params['IDs_only'] == True:
            result_list = wcsClient.execute_xml_request(self, http_request, IDs_only=True)
        else:
            result_list = wcsClient.execute_xml_request(self, http_request)
       
        return result_list
   
    
    #/************************************************************************/
    #/*                              GetCoverage()                           */
    #/************************************************************************/
    
    def GetCoverage(self, input_params):
        """
            
        """
        print "I'm in "+sys._getframe().f_code.co_name
        
        procedure_dict = self.set_base_getcov()
        http_request = self.create_request(input_params, procedure_dict)

        result = wcsClient.execute_getcov_request(self, http_request, input_params)
        
        return result


    #/************************************************************************/
    #/*                             parse_xml()                              */
    #/************************************************************************/ 
    def parse_xml(self, in_xml, tag):
        """
            Function to parse the request results (GetCapabilities & DescribeEOCoverageSet) for the available
            DataSetSeries (EOIDs) and CoveragesIDs.
        """
        print "I'm in "+sys._getframe().f_code.co_name
        
            # parse the xml - received as answer to the request
        xmldoc = minidom.parseString(in_xml)
            # find all the tags (CoverageIds or DatasetSeriesIds)
        tagid_node = xmldoc.getElementsByTagName(tag)
            # number of found tags
        n_elem = tagid_node.length
        tag_ids = []
            # store the found items
        for n  in range(0, n_elem):
            tag_ids.append(tagid_node[n].childNodes.item(0).data)
    
            # return the found items
        return tag_ids

    
    
    #/************************************************************************/
    #/*                         execute_xml_request()                        */
    #/************************************************************************/
    def execute_xml_request(self, http_request, IDs_only=False):
        """
            execute the generated request
        """
        print "I'm in "+sys._getframe().f_code.co_name

        try:
                # access the url
            request_handle = urllib2.urlopen(http_request)
                # read the content of the url
            result_xml = request_handle.read()

                # extract only the CoverageIDs and provide them as a list for further usage
            if IDs_only == True:
                cids = self.parse_xml(result_xml,  self.xml_ID_tag[1])
                request_handle.close()
                return cids
            else:
                request_handle.close()
            
        except urllib2.URLError, url_ERROR:
            if hasattr(url_ERROR, 'reason'):
                print  time.strftime("%Y-%m-%dT%H:%M:%S%Z"), "- ERROR:  Server not accessible -", url_ERROR.reason
            elif hasattr(url_ERROR, 'code'):
                print time.strftime("%Y-%m-%dT%H:%M:%S%Z"), "- ERROR:  The server couldn\'t fulfill the request - Code returned:  ", url_ERROR.code,  url_ERROR.read()
                err_msg = str(url_ERROR.code)+'--'+url_ERROR.read()
                return err_msg
                
        
        return result_xml

    #/************************************************************************/
    #/*                               execute_getcov_request()                           */
    #/************************************************************************/ 

    def execute_getcov_request(self, http_request, input_params):
        """
            execute the GetCoverage request(s)
        """
        now = time.strftime('_%Y%m%dT%H%M%S')
        if input_params.has_key('output'):
            outfile = input_params['output']+dsep+input_params['coverageID'][:-4]+now+input_params['coverageID'][-4:]
        else: 
            outfile = temp_storage+dsep+input_params['coverageID']
        
        try:
            res_getcov = urllib2.urlopen(http_request)
            status = res_getcov.code
            
            try:
                file_getcov = open(outfile, 'w+b')
                file_getcov.write(res_getcov.read())
                file_getcov.flush()
                os.fsync(file_getcov.fileno())
                file_getcov.close()
                res_getcov.close()
    
            except IOError as (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise


        except urllib2.URLError, url_ERROR:
            if hasattr(url_ERROR, 'reason'):
                print  time.strftime("%Y-%m-%dT%H:%M:%S%Z"), "- ERROR:  Server not accessible -", url_ERROR.reason
            elif hasattr(url_ERROR, 'code'):
                print time.strftime("%Y-%m-%dT%H:%M:%S%Z"), "- ERROR:  The server couldn\'t fulfill the request - Code returned:  ", url_ERROR.code,  url_ERROR.read()
                err_msg = str(url_ERROR.code)+'--'+url_ERROR.read()
                return err_msg
        except TypeError:
            pass

        return status
        
        
    #/************************************************************************/
    #/*                              merge_dicts()                           */
    #/************************************************************************/
    def merge_dicts(self, input_params, procedure_dict):
        """
            merge and harmonize the input_params-dict with the required request-dict
            e.g. the base_getcov-dict
        """
        print "I'm in "+sys._getframe().f_code.co_name
    
        request_dict={}
        for k,v in input_params.iteritems():
            if v == None or v == True:
                continue
            request_dict[k] = str(procedure_dict[k])+str(v)

        print len(request_dict)

            # get the basic request settings 
        base_request = self.set_base_request()
        request_dict.update(base_request)

        print len(request_dict)
    
    
        return request_dict



    #/************************************************************************/
    #/*                               create_request()                           */
    #/************************************************************************/
    def create_request(self, input_params, procedure_dict):
        """
            create the http-request according to the user selected Request-type
        """
        print "I'm in "+sys._getframe().f_code.co_name
      
        request_dict = self.merge_dicts(input_params, procedure_dict)
        
    ## here we could also validate the format of some of the input params provided eg. date/time, AOI, etc.
    #  eg. like checking the datevale for ISO and the timevalue for 'T00:00' and 'T23:59'
            # this doesn't look nice, but this way I can control the order within the generated request
        http_request=''
        if request_dict.has_key('server_url'):
            http_request=http_request+request_dict.get('server_url')
        if request_dict.has_key('service'):
            http_request=http_request+request_dict.get('service')
        if request_dict.has_key('version'):
            http_request=http_request+request_dict.get('version')
        
        if request_dict.has_key('request'):
            http_request=http_request+request_dict.get('request')
        if request_dict.has_key('coverageID'):
            http_request=http_request+request_dict.get('coverageID')
        if request_dict.has_key('subset_x'):
            http_request=http_request+request_dict.get('subset_x')+')'
        if request_dict.has_key('subset_y'):
            http_request=http_request+request_dict.get('subset_y')+')'
        if request_dict.has_key('format'):
            http_request=http_request+request_dict.get('format')
        if request_dict.has_key('rangesubset'):
            http_request=http_request+request_dict.get('rangesubset')
        if request_dict.has_key('outputcrs'):
            http_request=http_request+request_dict.get('outputcrs')
        if request_dict.has_key('interpolation'):
            http_request=http_request+request_dict.get('interpolation')
        if request_dict.has_key('mediatype'):
            http_request=http_request+request_dict.get('mediatype')
        if request_dict.has_key('size_x'):
            http_request=http_request+request_dict.get('size_x')+')'
        if request_dict.has_key('size_y'):
            http_request=http_request+request_dict.get('size_y')+')'
        if request_dict.has_key('mask'):
            http_request=http_request+request_dict.get('mask')+')'
            
        
        if request_dict.has_key('updateSequence'):
            http_request=http_request+request_dict.get('updateSequence')
        if request_dict.has_key('sections'):
            http_request=http_request+request_dict.get('sections')
        
        if request_dict.has_key('eoID'):
            http_request=http_request+request_dict.get('eoID')
#        if request_dict.has_key('subset_lat'):
#            http_request=http_request+request_dict.get('subset_lat')
#        if request_dict.has_key('subset_lon'):
#            http_request=http_request+request_dict.get('subset_lon')
        if request_dict.has_key('subset_time'):
            http_request=http_request+request_dict.get('subset_time').split(',')[0] \
                +'%22,%22'+request_dict.get('subset_time').split(',')[1]+'%22)'
        if request_dict.has_key('containment'):
            http_request=http_request+request_dict.get('containment')
        if request_dict.has_key('section'):
            http_request=http_request+request_dict.get('section')
        if request_dict.has_key('count'):
            http_request=http_request+request_dict.get('count')
        #if request_dict.has_key(''):
            #http_request=http_request+request_dict.get('')
    
    
        return http_request
    
    
    
    #/************************************************************************/
    #/*                              ()                           */
    #/************************************************************************/


#/************************************************************************/
####            END OF: wcs_Client class            #####                */
#/************************************************************************/
#/************************************************************************/


#/************************************************************************/
#/*                              get_cmdline()                           */
#/************************************************************************/
def get_cmdline(args):
    """
        handles the input from the commandline, help, and usage
    """
    print "I'm in "+sys._getframe().f_code.co_name
    
    class chk_input(argparse.Action):
        def __call__(self,cl_parser,namespace,  values, option_string=None):
            print 'Value','%r' % (values)
            print 'Option','%r' % (option_string)
            print 'Dest', self.dest
    
    class reformat_outsize(argparse.Action):
        def __call__(self,cl_parser,namespace,  values, option_string=None):
            out=''
            if values[0].startswith('siz'):
                out='size='+values[1]
            if values[0].startswith('res'):
                out='resolution='+values[1]

            setattr(namespace, self.dest, out)

##TODO - add some input checking
#    class chk_coord(argparse.Action):
#        def __call__(self,cl_parser,namespace,  values, option_string=None):
#            pass
#            
#    class chk_time(argparse.Action):
#        def __call__(self,cl_parser,namespace,  values, option_string=None):
#            pass
#        
#    class chk_CRS(argparse.Action):
#        def __call__(self,cl_parser,namespace,  values, option_string=None):
#           pass
    
    class cnv2str(argparse.Action):
        def __call__(self,cl_parser,namespace,  values, option_string=None):
            out=",".join(values)
            setattr(namespace, self.dest, out)
           
            

        # Common to all subparsers
    common_parser = argparse.ArgumentParser(add_help=False, version='%(prog)s'+':   '+ __version__)

    cl_parser = argparse.ArgumentParser(description='WCS 2.0.1/EO-WCS Client routine', parents=[common_parser])
    subparsers = cl_parser.add_subparsers(help='Requests', dest='request')


        # ==== GetCapabilities parameters
    getcap_parser = subparsers.add_parser('GetCapabilities', parents=[common_parser], 
                        help='send a GetCapabilities request')

          # Mandatory parameters
    mandatory = getcap_parser.add_argument_group('Mandatory')
    mandatory.add_argument('-s','--server_url', metavar='server_url', dest='server_url', action='store', 
                         required=True, help='the SERVER URL to be contaced')

        # Optional parameters
    getcap_parser.add_argument('--updateSequence', metavar='[Date_of_Change]', dest='updateSequence',  action='store', 
                        help='to receive a new document only if it has changed since last requested (expressed in ISO-8601 e.g. 2007-04-05)' )

    getcap_parser.add_argument('--sections', dest='sections', nargs='*', choices=['DatasetSeriesSummary', 'CoverageSummary', \
                        'Contents','ServiceIdentification','ServiceProvider','OperationsMetadata','Languages','All'],
                        help='request one or more section(s) of a Capabilities Document; NOTE: multiple sections need to \
                        be supplied within {};  [default=All]', action=cnv2str)                  


        # ==== DescribeCoverage parameters
    desccov_parser = subparsers.add_parser('DescribeCoverage', parents=[common_parser],  
                        help='send a DescribeCoverage request')

          # Mandatory parameters
    mandatory = desccov_parser.add_argument_group('Mandatory')

    mandatory.add_argument('-s','--server_url', metavar='server_url', dest='server_url', action='store', 
                         required=True, help='the SERVER URL which should be contaced')

    mandatory.add_argument('--coverageID', metavar='coverageID', required=True, 
                        help='a valid coverageID or StitchedMosaic')


        # ==== DescribeEOCoverageSet parameters
    desceocov_parser = subparsers.add_parser('DescribeEOCoverageSet', parents=[common_parser], 
                        help='DescribeEOCoverageSet')

          # Mandatory parameters
    mandatory = desceocov_parser.add_argument_group('Mandatory')

    mandatory.add_argument('-s','--server_url', metavar='server_url', dest='server_url', action='store', 
                         required=True, help='the SERVER URL which should be contaced')

    mandatory.add_argument('--eoID', metavar='eoID', required=True, 
                        help='a valid ID of a: DatasetSeries, Coverage, or StitchedMosaic ')

        # Optional parameters
## TODO - need some check here for the the coordinates
    desceocov_parser.add_argument('--subset_lat', metavar='subset_lat', dest='subset_y', #action=chk_coord, 
                        help='Allows to constrain the request in Lat-dimensions. \
                        The spatial constraint is expressed in WGS84. ')

    desceocov_parser.add_argument('--subset_lon', metavar='subset_lon', dest='subset_x', #action=chk_coord,
                        help='Allows to constrain the request in Lon-dimensions. \
                        The spatial constraint is expressed in WGS84. ')

    desceocov_parser.add_argument('--subset_time', metavar='subset_time_interval', # action=chk_time,
                        help='Allows to constrain the request in Time-dimensions. The temporal \
                        constraint (Start,End) is expressed in ISO-8601 \
                        (e.g. -subset_time 2007-04-05T14:30Z,2007-04-07T23:59Z). ')

    desceocov_parser.add_argument('--containment', choices=['overlaps','contains'])

    desceocov_parser.add_argument('--count', metavar='count', help='Limits the maximum number of DatasetDescriptions returned')

    desceocov_parser.add_argument('--section', dest='section', choices=['DatasetSeriesSummary', 'CoverageSummary','All'],
                        nargs='+', help='request one or more section(s) of a DescribeEOCoverageSet Document; NOTE: multiple sections need to \
                        be supplied within {}; [default=All]', action=cnv2str)
                        
    desceocov_parser.add_argument('--IDs_only', dest='IDs_only', action='store_true', default=None,  help='Non standard parameter -  will \
                        provide only a listing of the available CoverageIDs; intended to feed directly into a GetCoverage loop')


        # ==== GetCoverage parameters
    getcov_parser = subparsers.add_parser('GetCoverage', parents=[common_parser],
                        help='request a coverage for download')

          # Mandatory parameters
    mandatory = getcov_parser.add_argument_group('Mandatory')

    mandatory.add_argument('-s','--server_url', metavar='server_url', dest='server_url', action='store', 
                        required=True, help='the SERVER URL which should be contaced')

    mandatory.add_argument('--coverageID', metavar='coverageID', required=True, help='a valid coverageID')

    mandatory.add_argument('--format', choices=['tiff', 'jpeg', 'png', 'gif'], 
                        required=True, help='requested format of coverage to be returned')

    mandatory.add_argument('-o','--output', metavar='output', dest='output', action='store', 
                        help='location where downloaded data shall be stored [currently set to: '+temp_storage+']')
    
        # Optional parameters    
#    getcov_parser.add_argument('-o','--output', metavar='output', dest='output', action='store', 
#                        help='location where donwloaded data shall be stored [currently set to: '+temp_storage+']') 

##TODO - solve the choice of pixel, origCRS and newCRS -- in the subset_x/subset_y
    getcov_parser.add_argument('--subset_x', metavar='subset_x', #action=chk_coord, 
                        help='Trimming of coverage in X-dimension (no slicing allowed!), \
                        either in: pixel coordinates [ x(400,200) ], coordinates without CRS (-> original projection) [ Lat(12,14) ], \
                        coordinates with CRS (-> reprojecting) [ Long,http://www.opengis.net/def/crs/EPSG/0/4326(17,17.4) ]')

    getcov_parser.add_argument('--subset_y', metavar='subset_y', #action=chk_coord, 
                        help='Trimming of coverage in Y-dimension (no slicing allowed!), \
                        either in: pixel coordinates, coordinates without CRS (-> original projection), \
                        coordinates with CRS (-> reprojecting) [ for examples, see subset_x ]')

    getcov_parser.add_argument('--rangesubset', metavar='rangesubset', help='Subsetting in the range domain (e.g. Band-Subsetting, e.g. 3,2,1)')

    getcov_parser.add_argument('--outputcrs', metavar='outputcrs', type=int,  #action=chk_CRS,
                        help='CRS for the requested output coverage, supplied as EPSG number [default=4326]')

    getcov_parser.add_argument('--size_x', nargs=2, action=reformat_outsize, metavar=('[size 100 |', 'resolution 15]'),
                        help='Mutually exclusive, enter either: size & integer dimension of the requested coverage or \
                        resolution & the dimension of one pixel in X-Dimension')

    getcov_parser.add_argument('--size_y', nargs=2, action=reformat_outsize, metavar=('[size 100 |', 'resolution 15]'),
                        help='Mutually exclusive, enter either: size & integer dimension of the requested coverage or \
                        resolution & dimension of one pixel in Y-Dimension')

    getcov_parser.add_argument('--interpolation', choices=['nearest','bilinear','average'], 
                        help='Interpolation method to be used [default=nearest]')

    getcov_parser.add_argument('--mediatype', choices=['multipart/mixed'], nargs='?', 
                        help='Coverage delivered directly as image file or enclosed in GML structure \
                        [default=parameter is not provided]')

    getcov_parser.add_argument('--mask', metavar='mask', help='Masking of coverage by polygon: define the polygon by a list of \
                        points (i.e. latitude and longitude values), e.g. lat1,lon1,lat2,lon2,...; \
                        make sure to close the polygon with the last pair of coordinates; CRS is optional; \
                        per default EPSG 4326 is assumed; use the subset parameter to crop the resulting coverage')


    input = cl_parser.parse_args(args[1:])
    input_params=input.__dict__

   
    return input_params
    

#/************************************************************************/
#/*                               main()                                 */
#/************************************************************************/

def main(args):
    """
        Main function - 
    """
    print "I'm in "+sys._getframe().f_code.co_name    
    
        # get all parameters provided via cmd-line
    input_params = get_cmdline(args)
    
    test_print(input_params)
    
        # execute the user selected Request-type 
    if input_params.has_key('request'):
        to_call = input_params.get('request')
#        print 'Request', to_call
    
    wcs_call = wcsClient()

#    from IPython import embed  
#    embed()  

    exec "result = wcs_call."+to_call+"(input_params)"
    

    print result
    





if __name__ == "__main__":
    sys.exit(main(sys.argv))




###############################################
# Examples: 
#
# (1a): cmd-line parameters
# ./wcs_client.py  GetCoverage -s  http://neso.cryoland.enveo.at/cryoland/ows? -coverageID FSC_0.005deg_201404080650_201404081155_MOD_panEU_ENVEOV2.1.00.tif \
# -subset_x 28,30 -subset_y 59,61 -format jpeg 
# (1b): corresponding http-request
# http://neso.cryoland.enveo.at/cryoland/ows?service=wcs&request=GetCoverage&version=2.0.1&coverageid=FSC_0.005deg_201404080650_201404081155_MOD_panEU_ENVEOV2.1.00.tif&subset=x,http://www.opengis.net/def/crs/EPSG/0/4326%2828,30%29&subset=y,http://www.opengis.net/def/crs/EPSG/0/4326%2859,61%29&format=image/jpeg
#
# (2a):
# ./wcs_client.py  DescribeEOCoverageSet -s http://neso.cryoland.enveo.at/cryoland/ows?  --eoID daily_FSC_PanEuropean_Optical --subset_lat 32,44  --subset_lon 11,33  --subset_time  2012-03-17,2012-03-19T12:00:00Z    -- IDs_only
# (2b): 
# http://neso.cryoland.enveo.at/cryoland/ows?service=wcs&version=2.0.0&request=describeeocoverageset&eoid=daily_FSC_PanEuropean_Optical&subset=phenomenonTime(%222012-03-17%22,%222012-03-19T12:00:00Z%22)&subset=Lat,http://www.opengis.net/def/crs/EPSG/0/4326(32,44)&subset=Long,http://www.opengis.net/def/crs/EPSG/0/4326(11,33)
#
###############################################


