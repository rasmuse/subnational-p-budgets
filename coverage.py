import pandas as pd
import geopandas
import eust
import fadn


def get_intersection_areas(a, b):
    """
    Calculate the intersection area of two geopandas DataFrames.
    """
    # Because geopandas.overlay() does not preserve index, we'll convert the
    # (possibly MultiIndex) indices of a and b into columns named "a_index"
    # and "b_index" before calling geopandas.overlay().
    # We also prepare a function restore_index() to call at the end.

    original_indices = {"a_index": a.index, "b_index": b.index}

    a = a[["geometry"]].reset_index(drop=True).rename_axis("a_index")
    b = b[["geometry"]].reset_index(drop=True).rename_axis("b_index")

    def restore_index(d):
        def get_level_replacement(level_name):
            level_values = d.index.get_level_values(level_name)
            return original_indices[level_name][level_values].to_frame(
                index=False
            )

        index = pd.concat(
            [get_level_replacement(level_name) for level_name in d.index.names],
            axis=1,
        ).pipe(pd.MultiIndex.from_frame)
        d = d.copy()
        d.index = index
        return d

    areas = (
        geopandas.overlay(a.reset_index(), b.reset_index(), how="intersection")
        .set_index(["a_index", "b_index"])
        .geometry.area.rename("x_area")
        .to_frame()
        .join(a.geometry.area.rename("a_area"))
        .join(b.geometry.area.rename("b_area"))
        .pipe(restore_index)
        .sort_index()
    )

    return areas


def get_coverage(a, b):
    """
    With the geometries in geopandas DataFrames a and b, calculate the
    area fraction of features in a covered by features in b. In other words,
    the result is the area of the a/b intersection divided by the area of a.
    """
    return get_intersection_areas(a, b).eval("x_area / a_area")


NUTS_SHP_PATH = "indata/NUTS_RG_20M_2013_3035.shp/NUTS_RG_20M_2013_3035.shp"
FADN_SHP_PATH = "indata/FADN_RICA_PL_2012_20M/FADN_RICA_PL_2012_20M.shp"

nuts_path = NUTS_SHP_PATH
fadn_path = FADN_SHP_PATH

nuts_data = geopandas.read_file(nuts_path).set_index("NUTS_ID")
fadn_data = geopandas.read_file(fadn_path).set_index("FADN_2012_")

nuts2 = nuts_data[lambda d: d.index.str.len() == 4]

nuts2_coverage = get_coverage(nuts2, fadn_data)
