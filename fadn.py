import zipfile
import pandas as pd

FADN_DATA_DIR = "indata/fadn20190531"

ZIP_PATH_TEMPLATE = "{data_dir}/{name}.zip"
INSIDE_ZIP_PATH_TEMPLATE = "SO/{name}.csv"
CSV_SEP = ";"

COUNTRY_REGEX = r"\((?P<country_code>[A-Z]{3})\) (?P<country_name>.+)"
REGION_REGEX = r"\(0*(?P<region_code>[0-9]+)\) (?P<region_name>.+)"


def _get_index_cols(name):
    return name.split(".")


def _year_index_replacement(year):
    return year.rename("year").astype(int)


def _country_index_replacement(country):
    return country.str.extract(COUNTRY_REGEX)


def _region_index_replacement(region):
    region_split = region.str.extract(REGION_REGEX)
    region_split["region_code"] = region_split["region_code"].astype(int)
    return region_split


_INDEX_REPLACEMENTS = {
    "YEAR": _year_index_replacement,
    "COUNTRY": _country_index_replacement,
    "REGION": _region_index_replacement,
}


def _clean_index(index):
    d = index.to_frame()

    new_cols = []
    for colname in d.columns:
        if colname in _INDEX_REPLACEMENTS:
            replacement_func = _INDEX_REPLACEMENTS[colname]
            old_col = d[colname]
            replacement = replacement_func(old_col)
            new_cols.append(replacement)

    return (
        pd.concat(new_cols, axis=1)
        .pipe(lambda df: df.set_index(list(df.columns)))
        .index
    )


def _clean(data):
    data = data.copy()
    if "COUNTRY" in data.index.names:
        data = data[data.index.get_level_values("COUNTRY").notnull()]
    if "REGION" in data.index.names:
        data = data[
            data.index.get_level_values("REGION") != "."
        ]  # remove whole-country data
    data.index = _clean_index(data.index)
    return data


def read_fadn_data(name, data_dir=FADN_DATA_DIR, clean=True):
    zip_path = ZIP_PATH_TEMPLATE.format(name=name, data_dir=data_dir)
    index_cols = _get_index_cols(name)
    with open(zip_path, "rb") as zip_file:
        with zipfile.ZipFile(zip_file) as virtual_dir:
            path = INSIDE_ZIP_PATH_TEMPLATE.format(name=name)

            with virtual_dir.open(path) as f:
                d = pd.read_csv(f, sep=CSV_SEP)
                if clean:
                    d = d.set_index(index_cols)
                    d = _clean(d)
                return d
