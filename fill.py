import pandas as pd

def get_level_num(s, level):
    assert level is not None
    if isinstance(level, int):
        return level
    num, = (i for i, name in enumerate(s.index.names) if name == level)
    return num


def get_aggregates(s, aggregates, level=None, skipna=False):
    assert isinstance(s, pd.Series)

    if level is None:
        return (
            pd.Series(
                {
                    parent: s.reindex(children).sum(skipna=skipna)
                    for parent, children in aggregates.items()
                }
            )
            .rename(s.name)
            .rename_axis(s.index.names)
        )

    level_num = get_level_num(s, level)
    original_names = s.index.names
    s = s.swaplevel(level_num)
    drop_how = "all" if skipna else "any"
    d = pd.DataFrame(
        {
            parent: s.reindex(children, level=level)
            .unstack()
            .dropna(how=drop_how)
            .sum(axis=1)
            for parent, children in aggregates.items()
        }
    ).stack().swaplevel(level_num).rename_axis(original_names)

    return d


def fill_aggregates(s, aggregates, iterate=False, **kwargs):
    do_more = True
    while do_more:
        aggregate_values = get_aggregates(s, aggregates, **kwargs)
        union_index = s.index.union(aggregate_values.index)

        num_additions = len(aggregate_values.index.difference(s.index))
        do_more = iterate and num_additions

        s = s.reindex(union_index).fillna(aggregate_values)

    return s
