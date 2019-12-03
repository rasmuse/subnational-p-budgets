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
