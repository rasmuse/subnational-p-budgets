NUTS_VERSION = 2010
DATA_YEAR = 2013
DEFAULT_NUTS_LEVEL = 2
NUTS_LEVEL_EXCEPTIONS = {
    "DE": 1  # German FSS livestock populations for 2013 are on NUTS1 level
}
EXCLUDED_NUTS = {
    "FR9",  # DÉPARTEMENTS D'OUTRE-MER (French Guiana, etc)
    "FR91",  # Guadeloupe
    "FR92",  # Martinique
    "FR93",  # Guyane
    "FR94",  # Réunion
    "ES63",  # Ceuta in North Africa,
    "ES64",  # Melilla in North Africa
    "UKI1",  # Inner London
}

NUTS_GIS_PATH = (
    f"indata/NUTS_RG_20M_{NUTS_VERSION}_3035.shp/"
    f"NUTS_RG_20M_{NUTS_VERSION}_3035.shp"
)
ENZ_GIS_PATH = "indata/enz/enz_v8.shp"
GRASSLAND_YIELD_ENZ_PATH = "indata/smit-2008-grassland-yields.csv"
GRASSLAND_YIELD_NUTS_PATH = "outdata/grassland_yield.csv"
LIVEDATE_EXCRETION_PATH = (
    "indata/Livedate_2014_Database N excretion factors.xlsx"
)
FADN_GIS_PATH = "indata/FADN_RICA_PL_2012_20M/FADN_RICA_PL_2012_20M.shp"
P_CONTENT_PATH = "indata/p-content.csv"

FADN_WEIGHTS_PATH = "outdata/fadn_weights_by_nuts.csv"
ENZ_WEIGHTS_PATH = "outdata/enz_weights_by_nuts.csv"
CROP_DATA_PATH = "outdata/crop_data.csv"
REFERENCE_AREAS_PATH = "outdata/reference_areas.csv"
HARVEST_PATH = "outdata/harvest.csv"
EXCRETION_PATH = "outdata/excretion.csv"
MINERAL_FERTILIZER_PATH = "outdata/mineral_fertilizer.csv"

GEOPLOT_XLIM = [2636000.0, 6526000.0]
GEOPLOT_YLIM = [1217000.0, 5421000.0]
