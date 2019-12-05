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


def get_share(a, b):
    """
    With the geometries in geopandas DataFrames a and b, calculate the
    area share of each a feature in each b feature. In other words, the result
    is the area of the a-b intersection divided by the area of b.
    """
    return get_intersection_areas(a, b).eval("x_area / b_area").rename("share")
