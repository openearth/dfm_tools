#!/usr/bin/env python

"""Tests for dfm_tools package environment"""

import pytest
#import inspect
import os

dir_tests = os.path.join(os.path.realpath(__file__), os.pardir)
dir_testoutput = os.path.join(dir_tests,'test_output')
if not os.path.exists(dir_testoutput):
    os.mkdir(dir_testoutput)
dir_testinput = os.path.join(r'c:/DATA/werkmap','dfm_tools_testdata')

statement_list = ['import os','import sys','import glob','import shutil','import scipy','import numpy','import datetime','import pandas','import matplotlib','import netCDF4','import click','import shapely','import shapely.geometry','from shapely.geometry import Point']
@pytest.mark.parametrize("statement", [pytest.param('%s'%(stat), id='%s'%(stat)) for stat in statement_list])
@pytest.mark.unittest
def test_import_libraries(statement):
    """
    tests whether shapely can be imported successfully, this is a problem in some environments
    in that case 'import shapely' works, but import 'shapely.geometry' fails
    """
    
    try:
        exec(statement)
        import_success = True
    except:
        print('cannot execute "%s" failed'%(statement))
        import_success = False
        if statement == 'import shapely.geometry' or statement == 'from shapely.geometry import Point':
            print('ERROR: cannot execute "%s", check known bugs on https://github.com/openearth/dfm_tools for a solution'%(statement))
    
    assert import_success == True

        
