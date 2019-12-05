import pandas as pd

COVERAGE_PATH = "outdata/nuts-enz.csv"
ENZ_YIELDS_PATH = "indata/smit-2008-grassland-yields.csv"
NUTS_YIELDS_PATH = "outdata/nuts-grassland-yields.csv"

if __name__ == "__main__":
    coverage = pd.read_csv(COVERAGE_PATH, index_col=["EnZ_name", "NUTS_ID"])
    enz_yield = pd.read_csv(ENZ_YIELDS_PATH, index_col="EnZ_name")["yield"]
    nuts_yield = (
        coverage["share"]
        .mul(enz_yield)
        .groupby("NUTS_ID")
        .sum()
        .rename("yield")
    )
    nuts_yield.to_csv(NUTS_YIELDS_PATH, header=True)

