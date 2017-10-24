"""Performs spatial analysis on crash data. Uses manually prepped county data which includes population counts
  2010-2017."""
import sys


import arcpy
import pandas as pd

# Using NAD 83 as coordinate system
spatial_ref = arcpy.SpatialReference(4269)
directory = sys.path[0]

workspace = '{0}\\DWI.gdb'.format(directory)
if arcpy.Exists(workspace):
    pass
else:
    arcpy.CreateFileGDB_management(directory, "DWI")
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True
counties = '{0}\\counties'.format(workspace)
data_years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
county_list = []

# Build county list
with arcpy.da.SearchCursor(counties, ["CNTY_NM"]) as cursor1:
    for row in cursor1:
        county_list.append(row[0])


def county_deaths():
    """Joins prepped alcohol related crash data points with county polygons to find number of deaths per capita in each
    county for year on year trend analysis and to find enforcement patterns on a regional scale"""
    arcpy.MakeFeatureLayer_management("Master_DWIpoints", "Master_lyr")

    # Dictionary of dictionaries for building and assigning individual county stats into single feature class.
    data_dict_deaths = {name: {} for name in county_list}
    for key in data_dict_deaths:
        data_dict_deaths[key] = {year: 0 for year in data_years}

    for year in data_years:
        # Calculate county death counts for each year and save to new fc
        arcpy.SelectLayerByAttribute_management(in_layer_or_view="Master_lyr", selection_type="NEW_SELECTION",
                                                where_clause="Crash_Year = {0}".format(year))
        arcpy.SpatialJoin_analysis(target_features=counties, join_features="Master_lyr",
                                   out_feature_class='countydeaths{0}'.format(year),
                                   join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",
                                   field_mapping="CNTY_NM 'CNTY_NM' true true false 13 Text 0 0 ,First,#," + counties + ",CNTY_NM,-1,-1;CNTY_NBR 'CNTY_NBR' true true false 2 Short 0 0 ,First,#," + counties + ",CNTY_NBR,-1,-1;FIPS 'FIPS' true true false 2 Short 0 0 ,First,#," + counties + ",FIPS,-1,-1;pop{0} 'pop{1}' true true false 4 Long 0 0 ,First,#,".format(year, year) + counties + ",pop{0},-1,-1;Crash_Death_Count 'Crash_Death_Count{1}' true true false 4 Long 0 0 ,Sum,#,Master_DWIpoints,Crash_Death_Count,-1,-1".format(year, year),
                                   match_option='CONTAINS')
        # Add per capita (1000) field with 5 decimal places
        arcpy.AddField_management('countydeaths{0}'.format(year), "DeathsPer1000{0}".format(year), "DOUBLE",
                                  field_scale=5)
        # Calculate alcohol related crash deaths per 1000 people in field
        arcpy.CalculateField_management(in_table='countydeaths{0}'.format(year), field="DeathsPer1000{0}".format(year),
                                        expression="calcdeathrate( !Crash_Death_Count!, !pop{0}!)".format(year),
                                        expression_type="PYTHON_9.3",
                                        code_block="def calcdeathrate(death, pop):\n    if death == 0 or death is None:\n        return 0\n    else:\n        rate = float(death)/(float( pop)/1000)\n        return rate")

        with arcpy.da.SearchCursor('countydeaths{0}'.format(year), ["CNTY_NM", "DeathsPer1000{0}".format(year)]) as cursor1:
            for row in cursor1:
                data_dict_deaths[row[0]][year] = row[1]
    # Convert to data frame and save as csv
    county_df = pd.DataFrame.from_dict(data_dict_deaths)
    county_df.to_csv('{0}\CSVResults\CountyDeaths.csv'.format(directory))


def county_injuries():
    """Joins prepped alcohol related crash data points with county polygons to find number of injuries per capita in each
    county for year on year trend analysis and to find enforcement patterns on a regional scale"""
    arcpy.MakeFeatureLayer_management("Master_DWIpoints", "Master_lyr")

    # Dictionary of dictionaries for building and assigning individual county stats into single feature class.
    data_dict_injuries = {name: {} for name in county_list}
    for key in data_dict_injuries:
        data_dict_injuries[key] = {year: 0 for year in data_years}

    for year in data_years:
        # Calculate county injury counts for each year and save to new fc
        arcpy.SelectLayerByAttribute_management(in_layer_or_view="Master_lyr", selection_type="NEW_SELECTION",
                                                where_clause="Crash_Year = {0} AND Crash_Severity <> 'Not Injured' AND Crash_Severity <> 'Unknown'".format(year))
        arcpy.SpatialJoin_analysis(target_features=counties, join_features="Master_lyr",
                                   out_feature_class='countyinjuries{0}'.format(year),
                                   join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",
                                   field_mapping="CNTY_NM 'CNTY_NM' true true false 13 Text 0 0 ,First,#," + counties + ",CNTY_NM,-1,-1;CNTY_NBR 'CNTY_NBR' true true false 2 Short 0 0 ,First,#," + counties + ",CNTY_NBR,-1,-1;FIPS 'FIPS' true true false 2 Short 0 0 ,First,#," + counties + ",FIPS,-1,-1;pop{0} 'pop{1}' true true false 4 Long 0 0 ,First,#,".format(year, year) + counties + ",pop{0},-1,-1;Crash_Severity 'Crash_Severity{1}' true true false 8000 Text 0 0 ,Count,#,Master_DWIpoints,Crash_Severity,-1,-1".format(year, year),
                                   match_option='CONTAINS')
        arcpy.AddField_management('countyinjuries{0}'.format(year), "InjuriesPer1000{0}".format(year), "DOUBLE",
                                  field_scale=5)
        arcpy.CalculateField_management(in_table='countyinjuries{0}'.format(year), field="InjuriesPer1000{0}".format(year),
                                        expression="calcinjuryrate( !Crash_Severity!, !pop{0}!)".format(year),
                                        expression_type="PYTHON_9.3",
                                        code_block="def calcinjuryrate(injuries, pop):\n    if injuries == 0 or injuries is None:\n        return 0\n    else:\n        rate = float(injuries)/(float( pop)/1000)\n        return rate")

        with arcpy.da.SearchCursor('countyinjuries{0}'.format(year), ["CNTY_NM", "InjuriesPer1000{0}".format(year)]) as cursor2:
            for row in cursor2:
                data_dict_injuries[row[0]][year] = row[1]

        # Convert to data frame and save as csv
        county_df = pd.DataFrame.from_dict(data_dict_injuries)
        county_df.to_csv('{0}\CSVResults\CountyInjuries.csv'.format(directory))

county_injuries()
