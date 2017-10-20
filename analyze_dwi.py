"""Performs spatial analysis on crash data. Uses manually prepped county data which includes population counts
  2010-2017."""
import sys


import arcpy

# Using NAD 83 as coordinate system
spatial_ref = arcpy.SpatialReference(4269)
directory = sys.path[0]


def county_deaths():
    """Joins prepped DWI crash data points with county polygons to find number of deaths per capita in each county for
     year on year trend analysis and to elucidate enforcement patterns on a regional scale"""
    data_years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
    workspace = '{0}\\DWI.gdb'.format(directory)
    if arcpy.Exists(workspace):
        pass
    else:
        arcpy.CreateFileGDB_management(directory, "DWI")
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    arcpy.SpatialJoin_analysis()