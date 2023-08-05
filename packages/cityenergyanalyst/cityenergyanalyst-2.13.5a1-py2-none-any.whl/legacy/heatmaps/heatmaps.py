"""
Heatmapping algorithm
"""
from __future__ import division

import os
import pandas as pd

import cea.inputlocator
import cea.globalvar
import cea.config
from cea.interfaces.arcgis.modules import arcpy

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Daren Thomas"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def heatmaps(locator, analysis_fields, file_to_analyze):
    """
    algorithm to calculate heat maps out of n variables of interest

    :param file_to_analyze: path to the file with the variables to be mapped. This is used as the ``in_rows`` parameter
        to ``arcpy.CopyRows_management``, so anything supported by that tool could, in theory, work, but
        we use the csv files. Either the ``Total_Demand.csv`` file produced by the demand script or one of
        the files in the emissions results folder.
    :param analysis_fields:  when the path variables is selected, an array of n variables 'string'
        will be elaborated based on the selection of n input fields. For this a
        form like the one used in the Arcgis function ``merge/FieldMap`` could
        be used.

    :returns: - heat map of variable n: .tif
              - heat map file per variable of interest n.
    """
    arcpy.env.overwriteOutput = True
    arcpy.CheckOutExtension("Spatial")

    # figure out folder for the results based on file to analyze
    if locator.are_equal(file_to_analyze, locator.get_total_demand()):
        path_results = locator._ensure_folder(locator.get_plots_folder('heatmaps'))
    elif locator.are_equal(os.path.dirname(file_to_analyze), locator.get_lca_emissions_results_folder()):
        path_results = locator._ensure_folder(locator.get_plots_folder('heatmaps'))
    else:
        raise ValueError(
            'file_to_analyze must be either the demand totals file or a file in the emissions results folder: %s'
            % file_to_analyze)
    
    # local variables
    # create dbf file
    tempfile_name = "tempfile"
    tempfile = locator.get_temporary_file('tempfile.shp')
    tempfile_db_name = "data"
    tempfile_db = locator.get_temporary_file('data.dbf')

    gis_field_lookup = {}  # map csv_field -> gis_field

    # create a csv file in temp folder with gis_field names and only the analysis-fields (+ 'Name')
    export_fields = ['Name'] + analysis_fields
    file_to_analyse_df = pd.read_csv(file_to_analyze)[export_fields]
    file_to_analyse_df.columns = [get_gis_field(c, gis_field_lookup) for c in file_to_analyse_df.columns]
    tempfile_csv = locator.get_temporary_file('data.csv')
    file_to_analyse_df.to_csv(tempfile_csv)

    print('Copying rows from tempfile_csv={tempfile_csv} to out_table={tempfile_db}'.format(
        tempfile_csv=tempfile_csv, tempfile_db=tempfile_db))
    if os.path.exists(tempfile_db):
        os.remove(tempfile_db)
    arcpy.CopyRows_management(tempfile_csv, out_table=tempfile_db)

    arcpy.FeatureToPoint_management(locator.get_zone_geometry(), tempfile, "CENTROID")
    arcpy.MakeFeatureLayer_management(tempfile, "lyr", "#", "#")


    for csv_field in analysis_fields:
        gis_field = get_gis_field(csv_field, gis_field_lookup)
        arcpy.AddField_management("lyr", gis_field, "DOUBLE", "#", "#", "#", "#", "NULLABLE", "NON_REQUIRED", "#")

    # vector.append([])
    arcpy.AddJoin_management("lyr", "Name", tempfile_db, "Name", "KEEP_ALL")
    for csv_field in analysis_fields:
        gis_field = get_gis_field(csv_field, gis_field_lookup)
        arcpy.CalculateField_management(in_table="lyr", field="%(tempfile_name)s.%(gis_field)s" % locals(),
                                        expression="calc_non_null(!%(tempfile_db_name)s.%(gis_field)s!)" % locals(),
                                        expression_type="PYTHON_9.3",
                                        code_block="def calc_non_null(x):\n     if x is None:\n         return 0\n     elif x == '':\n         return 0\n     else:\n         return x\n")

    # calculate heatmaps
    for csv_field in analysis_fields:
        gis_field = get_gis_field(csv_field, gis_field_lookup)
        arcpy.gp.Idw_sa(tempfile, gis_field, os.path.join(path_results, gis_field), "1", "2", "VARIABLE 12")


def get_gis_field(csv_field, gis_field_lookup):
    """return a (max) 10 character representation of csv_field that is unique to the list of analysis fields"""
    import string
    if csv_field in gis_field_lookup:
        return gis_field_lookup[csv_field]
    gis_field_set = set(gis_field_lookup.values())
    gis_field = csv_field[:10]
    chars = iter(string.ascii_uppercase)
    while gis_field in gis_field_set:
        letters = list(gis_field)
        try:
            letters[-1] = next(chars)
        except StopIteration:
            raise Exception('Too many fields for analysis')
        gis_field = ''.join(letters)
    return gis_field

def main(config):
    assert os.path.exists(config.scenario), 'Scenario not found: %s' % config.scenario
    locator = cea.inputlocator.InputLocator(scenario=config.scenario)

    print('Running heatmaps with scenario = %s' % config.scenario)
    # print('Running heatmaps with file-to-analyze = %s' % config.heatmaps.file_to_analyze)
    analysis_fields = ['QH_sys_MWhyr', 'QC_sys_MWhyr', 'E_sys_MWhyr']
    # print('Running heatmaps with analysis-fields = %s' % config.heatmaps.analysis_fields)
    file_to_analyze = locator.get_total_demand()

    heatmaps(locator=locator, analysis_fields=analysis_fields, file_to_analyze=file_to_analyze)

    analysis_fields = ['O_ghg_ton', 'O_ghg_kgm2', 'O_nre_pen_GJ', 'O_nre_pen_MJm2']
    file_to_analyze = locator.get_lca_operation()

    heatmaps(locator=locator, analysis_fields=analysis_fields, file_to_analyze=file_to_analyze)

if __name__ == '__main__':
    main(cea.config.Configuration())
