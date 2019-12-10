import pandas as pd
import eust
import hierarchy
import settings


def get_nuts_candidates():
    return (
        eust.read_nuts_codes(settings.NUTS_VERSION, drop_extra_regio=True)
        .loc[lambda d: d.nuts_level <= 2]
        .loc[lambda d: ~d.index.isin(settings.EXCLUDED_NUTS)]
    )


def get_nuts_aggregates():
    nd = get_nuts_candidates()
    return {parent: list(g.index) for parent, g in nd.groupby("parent_geo")}


def fill_nuts(s):
    aggregates = get_nuts_aggregates()
    child_parent_pairs = {
        children[0]: [parent]
        for parent, children in aggregates.items()
        if len(children) == 1
    }
    return s.pipe(
        hierarchy.fill_sum_aggregates,
        aggregates,
        level="geo",
        skipna=False,
        iterate=True,
    ).pipe(
        hierarchy.fill_sum_aggregates,
        child_parent_pairs,
        level="geo",
        skipna=False,
        iterate=True,
    )


def filter_nuts_level(d, nuts_level, level="geo"):
    d_geo_index = (
        d.index
        if d.index.nlevels == 1
        else d.index.get_level_values(level)
    )
    codes = (
        eust.read_nuts_codes(settings.NUTS_VERSION)
        .nuts_level.loc[lambda s: s == nuts_level]
        .index
    )

    is_match = d_geo_index.isin(codes)

    return d[is_match]
