import sys

import arcpy

directory = sys.path[0]
csv = '{0}\\DWI.csv'.format(directory)
workspace = '{0}\\DWI.gdb'.format(directory)
table = 'tblDWI'


def parse_csv(csv, workspace):
    """Parses query results from CRIS and converts to GIS format. Exports three feature classes to workspace geodatabase;
    Crashes with no injuries, crashes with injuries and crashes with deaths."""

    if arcpy.Exists(workspace):
        arcpy.Delete_management(workspace)
        arcpy.CreateFileGDB_management(workspace, "DWI")

    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True
    # Prep CSV by converting lat long to float and removing NaN
    arcpy.TableToTable_conversion(in_rows=csv,
                                  out_path=workspace,
                                  out_name=table, where_clause="",
                                  field_mapping="Crash_ID 'Crash_ID' true true false 4 Long 0 0 ,First,#," + csv + ",Crash ID,-1,-1;Agency 'Agency' true true false 8000 Text 0 0 ,First,#," + csv + ",Agency,-1,-1;Case_ID 'Case_ID' true true false 8000 Text 0 0 ,First,#," + csv + ",Case ID,-1,-1;City 'City' true true false 8000 Text 0 0 ,First,#," + csv + ",City,-1,-1;County 'County' true true false 8000 Text 0 0 ,First,#," + csv + ",County,-1,-1;Crash_Death_Count 'Crash_Death_Count' true true false 4 Long 0 0 ,First,#," + csv + ",Crash Death Count,-1,-1;Crash_Severity 'Crash_Severity' true true false 8000 Text 0 0 ,First,#,"+ csv +",Crash Severity,-1,-1;Crash_Time 'Crash_Time' true true false 4 Long 0 0 ,First,#," + csv + ",Crash Time,-1,-1;Crash_Year 'Crash_Year' true true false 4 Long 0 0 ,First,#," + csv + ",Crash Year,-1,-1;Day_of_Week 'Day_of_Week' true true false 8000 Text 0 0 ,First,#," + csv + ",Day of Week,-1,-1;Intersecting_Street_Name 'Intersecting_Street_Name' true true false 8000 Text 0 0 ,First,#," + csv + ",Intersecting Street Name,-1,-1;Intersecting_Street_Number 'Intersecting_Street_Number' true true false 8000 Text 0 0 ,First,#," + csv + ",Intersecting Street Number,-1,-1;Latitude 'Latitude' true true false 8000 Text 0 0 ,First,#," + csv + ",Latitude,-1,-1;Longitude 'Longitude' true true false 8000 Text 0 0 ,First,#," + csv + ",Longitude,-1,-1;Street_Name 'Street_Name' true true false 8000 Text 0 0 ,First,#," + csv + ",Street Name,-1,-1;Street_Number 'Street_Number' true true false 8000 Text 0 0 ,First,#," + csv + ",Street Number,-1,-1;Charge 'Charge' true true false 8000 Text 0 0 ,First,#," + csv + ",Charge,-1,-1;Citation 'Citation' true true false 8000 Text 0 0 ,First,#," + csv + ",Citation,-1,-1",
                                  config_keyword="")

    arcpy.TableToTable_conversion(in_rows=table,
                                  out_path=workspace,
                                  out_name="DWIclean", where_clause="Latitude <> 'No Data' AND Longitude <> 'No Data'",
                                  field_mapping="Crash_ID 'Crash_ID' true true false 4 Long 0 0 ,First,#," + "{0}\\{1}".format(workspace, table) + ",Crash_ID,-1,-1;Agency 'Agency' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace, table) + ",Agency,-1,-1;Case_ID 'Case_ID' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Case_ID,-1,-1;City 'City' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",City,-1,-1;County 'County' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",County,-1,-1;Crash_Death_Count 'Crash_Death_Count' true true false 4 Long 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Crash_Death_Count,-1,-1;Crash_Severity 'Crash_Severity' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Crash_Severity,-1,-1;Crash_Time 'Crash_Time' true true false 4 Long 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Crash_Time,-1,-1;Crash_Year 'Crash_Year' true true false 4 Long 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Crash_Year,-1,-1;Day_of_Week 'Day_of_Week' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Day_of_Week,-1,-1;Intersecting_Street_Name 'Intersecting_Street_Name' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Intersecting_Street_Name,-1,-1;Intersecting_Street_Number 'Intersecting_Street_Number' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Intersecting_Street_Number,-1,-1;Latitude 'Latitude' true true false 8000 Float 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Latitude,-1,-1;Longitude 'Longitude' true true false 8000 Float 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Longitude,-1,-1;Street_Name 'Street_Name' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Street_Name,-1,-1;Street_Number 'Street_Number' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Street_Number,-1,-1;Charge 'Charge' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Charge,-1,-1;Citation 'Citation' true true false 8000 Text 0 0 ,First,#," + "{0}\\{1}".format(workspace,table) + ",Citation,-1,-1",
                                  config_keyword="")
    # Using GCS_WGS_84 for now
    arcpy.MakeXYEventLayer_management(table="DWIclean", in_x_field="Longitude", in_y_field="Latitude",
                                      out_layer="DWI_lyr",
                                      spatial_reference="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision",
                                      in_z_field="")
    # Crashes without injuries
    arcpy.FeatureClassToFeatureClass_conversion(in_features="DWI_lyr",
                                                out_path=workspace,
                                                out_name="DWI_Incidents_NoInjury", where_clause="""Crash_Severity = 'Not Injured'""",
                                                field_mapping="""Crash_ID "Crash_ID" true true false 4 Long 0 0 ,First,#,DWI_lyr,Crash ID,-1,-1;Agency "Agency" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Agency,-1,-1;City "City" true true false 8000 Text 0 0 ,First,#,DWI_lyr,City,-1,-1;County "County" true true false 8000 Text 0 0 ,First,#,DWI_lyr,County,-1,-1;Crash_Death_Count "Crash_Death_Count" true true false 4 Long 0 0 ,First,#,DWI_lyr,Crash Death Count,-1,-1;Crash_Severity "Crash_Severity" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Crash Severity,-1,-1;Crash_Year "Crash_Year" true true false 4 Long 0 0 ,First,#,DWI_lyr,Crash Year,-1,-1;Day_of_Week "Day_of_Week" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Day of Week,-1,-1;Latitude "Latitude" true true false 8 Double 0 0 ,First,#,DWI_lyr,Latitude,-1,-1;Longitude "Longitude" true true false 8 Double 0 0 ,First,#,DWI_lyr,Longitude,-1,-1;Charge "Charge" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Charge,-1,-1""")
    # Crashes with injuries
    arcpy.FeatureClassToFeatureClass_conversion(in_features="DWI_lyr",
                                                out_path=workspace,
                                                out_name="DWI_Incidents_Injury", where_clause="""Crash_Severity <> 'Not Injured'""",
                                                field_mapping="""Crash_ID "Crash_ID" true true false 4 Long 0 0 ,First,#,DWI_lyr,Crash ID,-1,-1;Agency "Agency" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Agency,-1,-1;City "City" true true false 8000 Text 0 0 ,First,#,DWI_lyr,City,-1,-1;County "County" true true false 8000 Text 0 0 ,First,#,DWI_lyr,County,-1,-1;Crash_Death_Count "Crash_Death_Count" true true false 4 Long 0 0 ,First,#,DWI_lyr,Crash Death Count,-1,-1;Crash_Severity "Crash_Severity" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Crash Severity,-1,-1;Crash_Year "Crash_Year" true true false 4 Long 0 0 ,First,#,DWI_lyr,Crash Year,-1,-1;Day_of_Week "Day_of_Week" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Day of Week,-1,-1;Latitude "Latitude" true true false 8 Double 0 0 ,First,#,DWI_lyr,Latitude,-1,-1;Longitude "Longitude" true true false 8 Double 0 0 ,First,#,DWI_lyr,Longitude,-1,-1;Charge "Charge" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Charge,-1,-1""")
    # Crashes with deaths
    arcpy.FeatureClassToFeatureClass_conversion(in_features="DWI_lyr",
                                                out_path=workspace,
                                                out_name="DWI_Incidents_Deaths", where_clause="""Crash_Death_Count <> 0""",
                                                field_mapping="""Crash_ID "Crash_ID" true true false 4 Long 0 0 ,First,#,DWI_lyr,Crash ID,-1,-1;Agency "Agency" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Agency,-1,-1;City "City" true true false 8000 Text 0 0 ,First,#,DWI_lyr,City,-1,-1;County "County" true true false 8000 Text 0 0 ,First,#,DWI_lyr,County,-1,-1;Crash_Death_Count "Crash_Death_Count" true true false 4 Long 0 0 ,First,#,DWI_lyr,Crash Death Count,-1,-1;Crash_Severity "Crash_Severity" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Crash Severity,-1,-1;Crash_Year "Crash_Year" true true false 4 Long 0 0 ,First,#,DWI_lyr,Crash Year,-1,-1;Day_of_Week "Day_of_Week" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Day of Week,-1,-1;Latitude "Latitude" true true false 8 Double 0 0 ,First,#,DWI_lyr,Latitude,-1,-1;Longitude "Longitude" true true false 8 Double 0 0 ,First,#,DWI_lyr,Longitude,-1,-1;Charge "Charge" true true false 8000 Text 0 0 ,First,#,DWI_lyr,Charge,-1,-1""")


parse_csv(csv, workspace)
