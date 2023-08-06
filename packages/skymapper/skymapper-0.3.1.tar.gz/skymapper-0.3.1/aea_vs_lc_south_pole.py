# load projection and helper functions
import numpy as np
import skymapper as skm
import matplotlib.pylab as plt

plt.style.use('website')

def getCatalog(size=10000):
    # dummy catalog
    ra = np.random.uniform(size=size, low=0, high=90)
    dec = np.random.uniform(size=size, low=-90, high=-45)
    return ra, dec

def plotDensity(ra, dec, nside=1024, sep=5., figsize=None):

    # setup figure
    import matplotlib.cm as cm
    cmap = cm.YlOrRd
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(121, aspect='equal')

    # setup map: define AEA map optimal for given RA/Dec
    proj = skm.createConicMap(ax, ra, dec, proj_class=skm.AlbersEqualAreaProjection, bgcolor='white')

    # add lines and labels for meridians/parallels (separation 5 deg)
    meridians = np.arange(-90, 90+sep, sep)
    parallels = np.arange(0, 360+sep, sep)
    skm.setMeridianPatches(ax, proj, meridians, linestyle='-', lw=0.5, alpha=0.3, zorder=2)
    skm.setParallelPatches(ax, proj, parallels, linestyle='-', lw=0.5, alpha=0.3, zorder=2)
    skm.setMeridianLabels(ax, proj, meridians, loc="left", fmt=skm.pmDegFormatter)
    if dec.mean() > 0:
        skm.setParallelLabels(ax, proj, parallels, loc="bottom")
    else:
        skm.setParallelLabels(ax, proj, parallels, loc="top")
    ax.text(0.05, 0.95, 'Albers Equal-Area', ha='left', va='top', transform=ax.transAxes)

    # setup map: define AEA map optimal for given RA/Dec
    ax = fig.add_subplot(122, aspect='equal')
    proj = skm.createConicMap(ax, ra, dec, proj_class=skm.LambertConformalProjection, bgcolor='white')

    # add lines and labels for meridians/parallels (separation 5 deg)
    meridians = np.arange(-90, 90+sep, sep)
    parallels = np.arange(0, 360+sep, sep)
    skm.setMeridianPatches(ax, proj, meridians, linestyle='-', lw=0.5, alpha=0.3, zorder=2)
    skm.setParallelPatches(ax, proj, parallels, linestyle='-', lw=0.5, alpha=0.3, zorder=2)
    skm.setMeridianLabels(ax, proj, meridians, loc="left", fmt=skm.pmDegFormatter)
    if dec.mean() > 0:
        skm.setParallelLabels(ax, proj, parallels, loc="bottom")
    else:
        skm.setParallelLabels(ax, proj, parallels, loc="top")
    ax.text(0.05, 0.95, 'Lambert Conformal', ha='left', va='top', transform=ax.transAxes)

    # show (and save) ...
    fig.tight_layout()
    fig.show()
    return fig, ax, proj


if __name__ == "__main__":

    # load RA/Dec from catalog
    size = 100000
    ra, dec = getCatalog(size)

    # plot density in healpix cells
    nside = 64
    sep = 15
    fig, ax, proj = plotDensity(ra, dec, nside=nside, sep=sep, figsize=(8.16,3))
