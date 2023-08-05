# coding: utf-8
from TeXConfig import *
from skymapper import *
import fitsio
fits = fitsio.FITS('lens_gold_y1a1_v1.fits')
w = fits[1].where('DEC < - 35')
ra_dec = fits[1]['RA', 'DEC'][w]
fits.close()

# get count in healpix cells, restrict to non-empty cells
nside = 128
bc, ra, dec, vertices = getCountAtLocations(ra_dec['RA'], ra_dec['DEC'], nside=nside, return_vertices=True)

# setup figure
import matplotlib.cm as cm
cmap = cm.YlOrRd
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111, aspect='equal')

# setup map: define AEA map optimal for given RA/Dec
aea = createConicMap(ax, ra, dec, proj_class=LambertConformalProjection, pad=0.2)
# add lines and labels for meridians/parallels (separation 5 deg)
meridians = np.linspace(-90, 0, 10)
parallels = np.linspace(0, 360, 25)
setMeridianPatches(ax, aea, meridians, linestyle='-', lw=0.5, alpha=0.3, zorder=2)
setParallelPatches(ax, aea, parallels, linestyle='-', lw=0.5, alpha=0.3, zorder=2)
setMeridianLabels(ax, aea, meridians, loc="left", fmt=pmDegFormatter)
setParallelLabels(ax, aea, parallels, loc="top")

# add healpix counts from vertices
vmin = 1.
vmax = 2.
poly = plotHealpixPolygons(ax, aea, vertices, color=bc, vmin=vmin, vmax=vmax, cmap=cmap, zorder=1, rasterized=True)

# add colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2%", pad=0.0)
cb = plt.colorbar(poly, cax=cax)
cb.set_label('$n_g$ [arcmin$^{-2}$]')
ticks = np.linspace(vmin, vmax, 6)
cb.set_ticks(ticks)
cb.solids.set_edgecolor("face")

fig.tight_layout()
fig.show()
#plt.savefig('example2.pdf')
