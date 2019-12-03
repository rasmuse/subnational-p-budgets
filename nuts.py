import pandas as pd
import eust

NUTS_YEAR = 2016
DEFAULT_NUTS_LEVEL = 2
EXCEPTIONS = {
    "DE": 1, # Most agricultural statistics available only on NUTS1 level
    "EL": 0, # Data quality concerns below NUTS0
    "SI": 0, # Data quality concerns below NUTS0
    'CY': 0, # Has only one NUTS2 region, so NUTS0 resolution is also NUTS2
    'EE': 0, # Has only one NUTS2 region, so NUTS0 resolution is also NUTS2
    'LU': 0, # Has only one NUTS2 region, so NUTS0 resolution is also NUTS2
    'LV': 0, # Has only one NUTS2 region, so NUTS0 resolution is also NUTS2
    'MT': 0, # Has only one NUTS2 region, so NUTS0 resolution is also NUTS2
}

def get_nuts_codes():
    return eust.read_nuts_codes(NUTS_YEAR, drop_extra_regio=True)


def get_nuts_aggregates():
    nd = get_nuts_codes()
    return {
        parent: list(g.index)
        for parent, g in nd.groupby('parent_geo')
    }


def get_included_regions():
    nd = get_nuts_codes()

    nuts_levels = (
        pd.Series(
            {
                **{
                    country: DEFAULT_NUTS_LEVEL
                    for country in nd.country_code.unique()
                },
                **EXCEPTIONS,
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

