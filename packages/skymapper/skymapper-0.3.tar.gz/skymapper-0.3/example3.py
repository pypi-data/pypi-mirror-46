# load projection and helper functions
from skymapper import *

def getCountLocation(query=None, nside=512):
    fits = fitsio.FITS('sva1_gold_wl_comb_flags_v18.fits')
    if query is None:
        coords = fits[1]['ra','dec'][:]
    else:
        w = fits[1].where(query)
        coords = fits[1]['ra','dec'][w]
    ipix = hp.ang2pix(nside, (90-coords['dec'])/180*np.pi, coords['ra']/180*np.pi, nest=False)
    bc = np.bincount(ipix)
    pixels = np.nonzero(bc)[0]
    #bc = bc[bc>0] / hp.nside2resol(nside, arcmin=True)**2 # in arcmin^-2
    #theta, phi = hp.pix2ang(nside, pixels, nest=False)
    #lat = 90 - theta*180/np.pi
    #lon = phi*180/np.pi
    fits.close()
    #return bc, lat, lon
    return pixels

def getKappa(nside=512):
    coords = np.genfromtxt('k_ngmix_20.0_5.0.txt', names=True)

    return coords['RA'], coords['DEC'], coords['kE']

def getClusters():
    clusters = np.genfromtxt('cluster_for_peter.txt', names=True)
    return clusters

# setup figure
import matplotlib.cm as cm
cmap = cm.RdYlBu_r
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, aspect='equal')

# load scalar function
# here lensing convergence kappa [not implemented]
ra, dec, kappa = getKappa()

# setup map: define AEA map optimal for given RA/Dec
aea = createConicMap(ax, ra, dec, proj_class=LambertConformalProjection)
# add lines and labels for meridians/parallels (separation 5 deg)
meridians = np.linspace(-60, -45, 4)
parallels = np.linspace(60, 90, 7)
setMeridianPatches(ax, aea, meridians, linestyle=':', lw=0.5, zorder=2)
setParallelPatches(ax, aea, parallels, linestyle=':', lw=0.5, zorder=2)
setMeridianLabels(ax, aea, meridians, loc="left", fmt=pmDegFormatter)
setParallelLabels(ax, aea, parallels, loc="bottom", fmt=hourAngleFormatter)

# convert to map coordinates and plot a marker for each point
x,y = aea(ra, dec)
marker = 'h'
markersize = getMarkerSizeToFill(fig, ax, x,y) * 1.7
vmin,vmax = -0.01, 0.01
sc = ax.scatter(x,y, c=kappa, edgecolors='None', marker=marker, s=markersize, cmap=cmap, vmin=vmin, vmax=vmax, rasterized=True, zorder=1)

# overplot with another data set
# here clusters [not implemented]
clusters = getClusters()
x,y  = aea(clusters['RA'], clusters['DEC'])
scc = ax.scatter(x,y, c='None', edgecolors='k', linewidths=1, s=clusters['lambda'], marker='o', zorder=3)

# add colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.0)
cb = plt.colorbar(sc, cax=cax)
cb.set_label('matter density $\kappa_E$ [compared to cosmic mean]')
ticks = np.linspace(vmin, vmax, 5)
cb.set_ticks(ticks)
cb.set_ticklabels([('%.1f' % (100*t)) + '%'  for t in ticks])
cb.solids.set_edgecolor("face")

# show (and save) ...
fig.tight_layout()
fig.show()
#fig.savefig(imagefile)
