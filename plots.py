import settings


def adj_geoplot(ax):
    ax.set_xlim(settings.GEOPLOT_XLIM)
    ax.set_ylim(settings.GEOPLOT_YLIM)
    ax.axis('off')
