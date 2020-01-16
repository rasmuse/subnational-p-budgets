import settings
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches
import geopandas
import mapclassify
import seaborn as sns


DEFAULT_LEGEND_FMT = "{:.1f}"

CHOROPLETH_KWS = {
    "surplus": dict(
        bin_uls=[-5, 0, 5, 10, 15, 20],
        cmap=mpl.cm.viridis_r,
        legend_fmt="${:.0f}$",
    ),
    "mineral": dict(
        bin_uls=[5, 10, 15, 20],  # fmt: no
        cmap=mpl.cm.BuPu,
        legend_fmt="${:.0f}$",
    ),
    "harvest": dict(
        bin_uls=[5, 10, 15, 20, 25],  # fmt: no
        cmap=mpl.cm.Greens,
        legend_fmt="${:.0f}$",
    ),
    "excretion": dict(
        bin_uls=[5, 10, 15, 20, 25, 30],
        cmap=mpl.cm.inferno_r,
        legend_fmt="${:.0f}$",
    ),
}

# Figure sizes etc
COLWIDTH = 76 / 25.4 # 84?
TEXTWIDTH = 160 / 25.4 # 174?
# Max height 234?

sns.set_style('darkgrid')
sns.set(
    font="Arial",
    rc={
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "axes.titlesize": 9,
        "axes.labelsize": 8.5,
        "legend.title_fontsize": 8.5,
        "legend.fontsize": 8.5,
        "text.usetex": False,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial"],
        "mathtext.rm": "Arial",
        "mathtext.fontset": "custom",
        "axes.facecolor": "#eaeaea",
    },
)


def adjust_print_plot(fig, **kwargs):
    defaults = dict(left=0, bottom=0, right=1, top=0.97, wspace=0.05, hspace=0.05)

    fig.subplots_adjust(**{**defaults, **kwargs})


def adj_geoplot(ax):
    ax.set_xlim(settings.GEOPLOT_XLIM)
    ax.set_ylim(settings.GEOPLOT_YLIM)
    ax.axis("off")


def make_legend_handles(scheme, cmap, fmt=DEFAULT_LEGEND_FMT):
    colors = mpl.cm.ScalarMappable(
        cmap=cmap, norm=mpl.colors.Normalize()
    ).to_rgba(np.arange(len(scheme.bins)))

    texts = []

    ll = None

    for i, ul in enumerate(scheme.bins):
        if ll is None:
            text = "< " + fmt.format(ul)
        else:
            text = fmt.format(ll) + " - " + fmt.format(ul)
        ll = ul
        texts.append(text)

    patches = [
        matplotlib.patches.Patch(color=c, label=t)
        for c, t in zip(colors, texts)
    ]

    return patches[::-1]


def plot_choropleth(
    d,
    key,
    *,
    scheme=None,
    bin_uls=None,
    ax=None,
    cmap=mpl.cm.viridis_r,
    legend=True,
    legend_kws=None,
    legend_fmt=DEFAULT_LEGEND_FMT,
    plot_kws=None,
):
    if legend_kws is None:
        legend_kws = {}

    if plot_kws is None:
        plot_kws = {}

    if bin_uls is not None:
        assert scheme is None, "supply either scheme or bin_uls"
        scheme = mapclassify.UserDefined(d[key], bin_uls)

    assert scheme is not None

    if ax is None:
        fig, ax = plt.subplots()

    plot_data = d.assign(**{key: scheme.yb})
    plot_data.plot(key, cmap=cmap, ax=ax, linewidth=0, **plot_kws)

    if legend:
        handles = make_legend_handles(scheme, cmap, fmt=legend_fmt)
        ax.legend(handles=handles, **legend_kws)

    return ax


def plot_europe_background(ax=None):
    if ax is None:
        fig, ax = plt.subplots()

    europe = (
        geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
        .loc[lambda d: d.continent == "Europe"]
        .to_crs("EPSG:3035")
    )
    europe.plot(color="#cccccc", ax=ax, linewidth=0)

    return ax


def plot_europe_choropleth(d, key, ax=None, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()

    ax = plot_europe_background(ax=ax)
    ax = plot_choropleth(d, key, ax=ax, **kwargs)
    adj_geoplot(ax)

    return ax
