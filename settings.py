NUTS_VERSION = 2013
DEFAULT_NUTS_LEVEL = 2
NUTS_LEVEL_EXCEPTIONS = {
    "DE": 1,  # Most agricultural statistics available only on NUTS1 level
    "EL": 0,  # Data quality concerns below NUTS0
    "SI": 0,  # Data quality concerns below NUTS0
}
NUTS_GIS_PATH = "indata/NUTS_RG_20M_2013_3035.shp/NUTS_RG_20M_2013_3035.shp"
ENZ_GIS_PATH = "indata/enz/enz_v8.shp"
FADN_GIS_PATH = "indata/FADN_RICA_PL_2012_20M/FADN_RICA_PL_2012_20M.shp"

GEOPLOT_XLIM = [2636000., 6526000.]
GEOPLOT_YLIM = [1217000., 5421000.]

DATA_YEAR = 2013
