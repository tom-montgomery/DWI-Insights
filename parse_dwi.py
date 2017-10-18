# import sys

import arcpy

csv = 'C:\\Users\\140318\\Desktop\\Python\\Python3x\\DWI\\DWI.csv'
workspace = 'C:\\Users\\140318\\Desktop\\Python\\Python3x\\DWI\\DWI.gdb'


def parse_csv(csv, workspace):
    """Parses query results from CRIS and converts to GIS format"""

    # workspace = sys.path[0]
    if arcpy.Exists(workspace):
        pass
    else:
        arcpy.CreateFileGDB_management(workspace, "DWI")
    arcpy.env.workspace = '{0}\\DWI.gdb'.format(workspace)
    arcpy.env.overwriteOutput = True
    # Used GCS_WGS_84 as placeholder
    arcpy.MakeXYEventLayer_management(table=csv,
                                      in_x_field="Longitude", in_y_field="Latitude", out_layer="DWI_Layer",
                                      spatial_reference="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision",
                                      in_z_field="")
    arcpy.FeatureClassToFeatureClass_conversion(in_features="DWI_Layer",
                                                out_path=workspace,
                                                out_name="DWI_Incidents_NoInjury", where_clause="""Crash_Severity = 'Not Injured'""",
                                                field_mapping="""Crash_ID "Crash_ID" true true false 4 Long 0 0 ,First,#,DWIstripped2_Layer,Crash ID,-1,-1;Agency "Agency" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Agency,-1,-1;City "City" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,City,-1,-1;County "County" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,County,-1,-1;Crash_Death_Count "Crash_Death_Count" true true false 4 Long 0 0 ,First,#,DWIstripped2_Layer,Crash Death Count,-1,-1;Crash_Severity "Crash_Severity" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Crash Severity,-1,-1;Crash_Year "Crash_Year" true true false 4 Long 0 0 ,First,#,DWIstripped2_Layer,Crash Year,-1,-1;Day_of_Week "Day_of_Week" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Day of Week,-1,-1;Latitude "Latitude" true true false 8 Double 0 0 ,First,#,DWIstripped2_Layer,Latitude,-1,-1;Longitude "Longitude" true true false 8 Double 0 0 ,First,#,DWIstripped2_Layer,Longitude,-1,-1;Charge "Charge" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Charge,-1,-1""")
    arcpy.FeatureClassToFeatureClass_conversion(in_features="DWI_Layer",
                                                out_path=workspace,
                                                out_name="DWI_Incidents_Injury", where_clause="""Crash_Severity <> 'Not Injured'""",
                                                field_mapping="""Crash_ID "Crash_ID" true true false 4 Long 0 0 ,First,#,DWIstripped2_Layer,Crash ID,-1,-1;Agency "Agency" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Agency,-1,-1;City "City" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,City,-1,-1;County "County" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,County,-1,-1;Crash_Death_Count "Crash_Death_Count" true true false 4 Long 0 0 ,First,#,DWIstripped2_Layer,Crash Death Count,-1,-1;Crash_Severity "Crash_Severity" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Crash Severity,-1,-1;Crash_Year "Crash_Year" true true false 4 Long 0 0 ,First,#,DWIstripped2_Layer,Crash Year,-1,-1;Day_of_Week "Day_of_Week" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Day of Week,-1,-1;Latitude "Latitude" true true false 8 Double 0 0 ,First,#,DWIstripped2_Layer,Latitude,-1,-1;Longitude "Longitude" true true false 8 Double 0 0 ,First,#,DWIstripped2_Layer,Longitude,-1,-1;Charge "Charge" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Charge,-1,-1""")
    arcpy.FeatureClassToFeatureClass_conversion(in_features="DWI_Layer",
                                                out_path=workspace,
                                                out_name="DWI_Incidents_Deaths", where_clause="""Crash_Death_Count <> 0""",
                                                field_mapping="""Crash_ID "Crash_ID" true true false 4 Long 0 0 ,First,#,DWIstripped2_Layer,Crash ID,-1,-1;Agency "Agency" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Agency,-1,-1;City "City" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,City,-1,-1;County "County" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,County,-1,-1;Crash_Death_Count "Crash_Death_Count" true true false 4 Long 0 0 ,First,#,DWIstripped2_Layer,Crash Death Count,-1,-1;Crash_Severity "Crash_Severity" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Crash Severity,-1,-1;Crash_Year "Crash_Year" true true false 4 Long 0 0 ,First,#,DWIstripped2_Layer,Crash Year,-1,-1;Day_of_Week "Day_of_Week" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Day of Week,-1,-1;Latitude "Latitude" true true false 8 Double 0 0 ,First,#,DWIstripped2_Layer,Latitude,-1,-1;Longitude "Longitude" true true false 8 Double 0 0 ,First,#,DWIstripped2_Layer,Longitude,-1,-1;Charge "Charge" true true false 8000 Text 0 0 ,First,#,DWIstripped2_Layer,Charge,-1,-1""")


parse_csv(csv, workspace)
