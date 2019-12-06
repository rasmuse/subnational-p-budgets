import pandas as pd


def _get_pandas_level_num(s, level):
    assert level is not None
    if isinstance(level, int):
        return level
    num, = (i for i, name in enumerate(s.index.names) if name == level)
    return num


def sum_aggregates(s, aggregates, level=None, skipna=False):
    assert isinstance(s, pd.Series)

    if level is not None:
        if len(s.index.names) == 1:
            name, = s.index.names
            if name != level:
                raise ValueError(f"no level '{level}' present")
            level = None

    if level is None:
        return (
            pd.Series(
                {
                    dst_label: s.reindex(src_labels).sum(skipna=skipna)
                    for dst_label, src_labels in aggregates.items()
                }
            )
            .rename(s.name)
            .rename_axis(s.index.names)
        )

    level_num = _get_pandas_level_num(s, level)
    original_names = s.index.names
    s = s.swaplevel(level_num)
    drop_how = "all" if skipna else "any"
    d = (
        pd.DataFrame(
            {
                dst_label: s.reindex(src_labels, level=level)
                .unstack()
                .dropna(how=drop_how)
                .sum(axis=1)
                for dst_label, src_labels in aggregates.items()
            }
        )
        .stack()
        .swaplevel(level_num)
        .rename_axis(original_names)
    )

    return d


def _fill(s, func, *args, iterate=False, **kwargs):
    do_more = True
    while do_more:
        additions = func(s, *args, **kwargs)
        union_index = s.index.union(additions.index)

        num_additions = len(additions.index.difference(s.index))
        do_more = iterate and num_additions

        s = s.reindex(union_index).fillna(additions)

    return s


def fill_sum_aggregates(s, aggregates, iterate=False, **kwargs):
    return _fill(s, sum_aggregates, aggregates, iterate=iterate, **kwargs)


def copy_to_children(s, aggregates, level=None):
    assert isinstance(s, pd.Series)

    child_parent_pairs = {}
    for parent, children in aggregates.items():
        for child in children:
            if child in child_parent_pairs:
                raise ValueError(
                    f"item {child} has at least two parents: "
                    f"{child_parent_pairs[child]} and {parent}"
                )
            child_parent_pairs[child] = [parent]

    return sum_aggregates(s, child_parent_pairs, skipna=False, level=level)


def fill_copy_to_children(s, aggregates, iterate=False, **kwargs):
    return _fill(s, copy_to_children, aggregates, iterate=iterate, **kwargs)
