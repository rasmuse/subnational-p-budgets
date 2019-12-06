import pandas as pd
import eust
import hierarchy
import settings


def get_nuts_codes():
    return eust.read_nuts_codes(settings.NUTS_VERSION, drop_extra_regio=True)


def get_nuts_aggregates():
    nd = get_nuts_codes()
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


def get_included_regions():
    nd = get_nuts_codes()

    nuts_levels = (
        pd.Series(
            {
                **{
                    country: settings.DEFAULT_NUTS_LEVEL
                    for country in nd.country_code.unique()
                },
                **settings.NUTS_LEVEL_EXCEPTIONS,
            }
        )
        .rename("nuts_level")
        .rename_axis("country_code")
        .to_frame()
        .reset_index()
    )

    return (
        nd.reset_index()
        .merge(nuts_levels, on=["country_code", "nuts_level"])
        .set_index("geo")
        .index
    )
