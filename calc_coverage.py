from pathlib import Path
import coverage
import geopandas

OUTDIR = Path("outdata")

PATHS = {
    "nuts": "indata/NUTS_RG_20M_2013_3035.shp/NUTS_RG_20M_2013_3035.shp",
    "fadn": "indata/FADN_RICA_PL_2012_20M/FADN_RICA_PL_2012_20M.shp",
    "enz": "indata/enz/enz_v8.shp",
}

INDEX_COLS = {"nuts": "NUTS_ID", "fadn": "FADN_2012_", "enz": "EnZ_name"}

PAIRS = [
    ("nuts", "fadn"),  # to estimate mineral P rates in NUTS regions from FADN
    (
        "nuts",
        "enz",
    ),  # to estimate permanent grassland prod. from environmental zones
]


def get_out_path(a, b):
    return OUTDIR / f"{a}-{b}.csv"


def load_data(item):
    return geopandas.read_file(PATHS[item]).set_index(INDEX_COLS[item])


def get_coverage(a, b):
    return coverage.get_coverage(load_data(a), load_data(b))


if __name__ == "__main__":
    for pair in PAIRS:
        get_coverage(*pair).to_csv(get_out_path(*pair), header=True)
