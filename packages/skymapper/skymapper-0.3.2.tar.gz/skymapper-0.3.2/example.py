# coding: utf-8
from TeXConfig import *
from skymapper import *
import fitsio
fits = fitsio.FITS('lens_gold_y1a1_v1.fits')
w = fits[1].where('DEC < - 35')
ra_dec = fits[1]['RA', 'DEC'][w]
fits.close()
nside = 512
bc, ra, dec, vertices = getCountAtLocations(ra_dec['RA'], ra_dec['DEC'], nside=nside, return_vertices=True)
setTeXPlot(2)
import matplotlib.cm as cm
cmap = cm.YlOrRd
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111, aspect='equal')
aea = createAEAMap(ax, ra, dec)
meridians = np.linspace(-90, 0, 19)
parallels = np.linspace(0, 360, 25)
aea.setMeridianPatches(ax, meridians, linestyle=':', lw=0.5, zorder=1)
aea.setParallelPatches(ax, parallels, linestyle=':', lw=0.5, zorder=1)
aea.setMeridianLabels(ax, meridians, loc="left", fmt=pmDegFormatter)
aea.setParallelLabels(ax, parallels, loc="top", fmt=hourAngleFormatter)
vmin = 1
vmax = 2
poly = plotHealpixPolygons(ax, aea, vertices, color=bc, vmin=vmin, vmax=vmax, cmap=cmap, zorder=2, rasterized=True)
fits = fitsio.FITS('y1a1_gold_1.0.2b-full_run_redmapper_v6.4.11_lgt5_desformat_catalog.fit')
w = fits[1].where('LAMBDA_CHISQ > 40 && DEC < -35')
clusters = fits[1]['RA', 'DEC', 'LAMBDA_CHISQ'][w]
fits.close()
x,y = aea(clusters['RA'], clusters['DEC'])
scc = ax.scatter(x,y, c='#2B3856', s=clusters['LAMBDA_CHISQ']/5, edgecolors='None', linewidths=1, marker='o', rasterized=True, zorder=3)
import matplotlib.lines as lines
redsq = lines.Line2D([],[], marker='s', c=[cmap(0), cmap(128), cmap(230)], markeredgecolor='None', markersize=6, lw=0, label='lensing galaxies')
bluedot = lines.Line2D([],[], marker='o', c='#2B3856', markeredgecolor='None', markersize=6, lw=0, label='redMaPPer clusters, $\lambda > 40$')
leg = ax.legend(handles=[bluedot], loc='lower left', frameon=True, framealpha=0.5, numpoints=1, borderpad=0.4, handlelength=1, handletextpad=0.2)
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2%", pad=0.0)
cb = plt.colorbar(poly, cax=cax)
cb.set_label('$n_{gal}$ [arcmin$^{-2}$]')
ticks = np.linspace(vmin, vmax, 5)
cb.set_ticks(ticks)
cb.solids.set_edgecolor("face")
plt.tight_layout()
plt.show()
