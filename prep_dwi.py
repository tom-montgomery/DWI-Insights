import sys


import arcpy

# Using NAD 83 as coordinate system
spatial_ref = arcpy.SpatialReference(4269)
directory = sys.path[0]


def convert_to_points():
    """Parses query results from CRIS and converts to GIS point format. Exports feature classes for each year of TXDoT
    data."""
    workspace = '{0}\\DWI.gdb'.format(directory)
    # data_years = range(2010, 2018)
    data_years = range(2010, 2017)
    if arcpy.Exists(workspace):
        pass
    else:
        arcpy.CreateFileGDB_management(directory, "DWI")
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    for year in data_years:
        csv = '{0}\\CSVResults\\DWI_{1}.csv'.format(directory, year)
        table = 'tblDWI_{0}'.format(year)
        # Prep CSV by converting lat long to float and removing NaN
        arcpy.TableToTable_conversion(in_rows=csv, out_path=workspace, out_name=table,
                                      field_mapping="Crash_ID 'Crash_ID' true true false 4 Long 0 0 ,First,#," + csv + ",Crash ID,-1,-1;Agency 'Agency' true true false 8000 Text 0 0 ,First,#," + csv + ",Agency,-1,-1;City 'City' true true false 8000 Text 0 0 ,First,#," + csv + ",City,-1,-1;County 'County' true true false 8000 Text 0 0 ,First,#," + csv + ",County,-1,-1;Crash_Death_Count 'Crash_Death_Count' true true false 4 Long 0 0 ,First,#," + csv + ",Crash Death Count,-1,-1;Crash_Severity 'Crash_Severity' true true false 8000 Text 0 0 ,First,#," + csv + ",Crash Severity,-1,-1;Crash_Year 'Crash_Year' true true false 4 Long 0 0 ,First,#," + csv + ",Crash Year,-1,-1;Latitude 'Latitude' true true false 20 Text 0 0 ,First,#," + csv + ",Latitude,-1,-1;Longitude 'Longitude' true true false 20 Text 0 0 ,First,#," + csv + ",Longitude,-1,-1;Contributing_Factor_1 'Contributing_Factor_1' true true false 8000 Text 0 0 ,First,#," + csv + ",Contributing Factor 1,-1,-1;Contributing_Factor_2 'Contributing_Factor_2' true true false 8000 Text 0 0 ,First,#," + csv + ",Contributing Factor 2,-1,-1;Contributing_Factor_3 'Contributing_Factor_3' true true false 8000 Text 0 0 ,First,#," + csv + ",Contributing Factor 3,-1,-1;Driver_Alcohol_Result 'Driver_Alcohol_Result' true true false 8000 Text 0 0 ,First,#," + csv + ",Driver Alcohol Result,-1,-1;Charge 'Charge' true true false 8000 Text 0 0 ,First,#," + csv + ",Charge,-1,-1")
        arcpy.TableToTable_conversion(in_rows=table,
                                      out_path=workspace,
                                      out_name="{0}_".format(table),
                                      where_clause="Latitude <> 'No Data' AND Longitude <> 'No Data' ",
                                      field_mapping="Crash_ID 'Crash_ID' true true false 4 Long 0 0 ,First,#," + table + ",Crash_ID,-1,-1;Agency 'Agency' true true false 8000 Text 0 0 ,First,#," + table + ",Agency,-1,-1;City 'City' true true false 8000 Text 0 0 ,First,#," + table + ",City,-1,-1;County 'County' true true false 8000 Text 0 0 ,First,#," + table + ",County,-1,-1;Crash_Death_Count 'Crash_Death_Count' true true false 4 Long 0 0 ,First,#," + table + ",Crash_Death_Count,-1,-1;Crash_Severity 'Crash_Severity' true true false 8000 Text 0 0 ,First,#," + table + ",Crash_Severity,-1,-1;Crash_Year 'Crash_Year' true true false 4 Long 0 0 ,First,#," + table + ",Crash_Year,-1,-1;Latitude 'Latitude' true true false 20 Float 0 0 ,First,#," + table + ",Latitude,-1,-1;Longitude 'Longitude' true true false 20 Float 0 0 ,First,#," + table + ",Longitude,-1,-1;Contributing_Factor_1 'Contributing_Factor_1' true true false 8000 Text 0 0 ,First,#," + table + ",Contributing_Factor_1,-1,-1;Contributing_Factor_2 'Contributing_Factor_2' true true false 8000 Text 0 0 ,First,#," + table + ",Contributing_Factor_2,-1,-1;Contributing_Factor_3 'Contributing_Factor_3' true true false 8000 Text 0 0 ,First,#," + table + ",Contributing_Factor_3,-1,-1;Driver_Alcohol_Result 'Driver_Alcohol_Result' true true false 8000 Text 0 0 ,First,#," + table + ",Driver_Alcohol_Result,-1,-1;Charge 'Charge' true true false 8000 Text 0 0 ,First,#," + table + ",Charge,-1,-1")
        # Convert to XY points
        arcpy.MakeXYEventLayer_management("{0}_".format(table), "Longitude", "Latitude", "DWI_{0}".format(year),
                                          spatial_ref)
        arcpy.FeatureClassToFeatureClass_conversion("DWI_{0}".format(year), workspace, "DWIpoints_{0}".format(year))

        # Create master point fc
        if year == 2010:
            arcpy.CreateFeatureclass_management(workspace, "Master_DWIpoints", "POINT", "DWIpoints_{0}".format(year),
                                                spatial_reference=spatial_ref)
            arcpy.Append_management("DWIpoints_{0}".format(year), "Master_DWIpoints", "NO_TEST")
        else:
            arcpy.Append_management("DWIpoints_{0}".format(year), "Master_DWIpoints", "NO_TEST")
        # Delete records with duplicate CrashID
        arcpy.DeleteIdentical_management(in_dataset="Master_DWIpoints", fields="Crash_ID")

        arcpy.Delete_management("DWIpoints_{0}".format(year))
        # Clean up geodatabase
        arcpy.Delete_management(table)
        arcpy.Delete_management("{0}_".format(table))


# convert_to_points()
