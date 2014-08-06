from __future__ import division
import numpy as np
import healpy as hp
from astropy.table import Table, vstack
import matplotlib.pyplot as plt


def hp_count_map(radecdata, nside, weights=None, nest=False):
    """
    Creates a Healpix object count map from a 2d array of RA, DEC positions

    fixme-fixme-fixme 
    """

    # Sanity checks

    if weights is not None:
        assert len(weights) == len(radecdata), ("Weights and data must have " +
                                                "the same length")

    assert (nside & (nside-1)) == 0 and nside != 0, ("nside must be a power " +
                                                     "of 2")

    # Assign each galaxy to a Healpix pixel
    deg2rad = np.pi/180
    theta = deg2rad*(90.0 - radecdata[:,1])
    phi = deg2rad*radecdata[:,0]
    gal_hppix = hp.ang2pix(nside, theta=theta, phi=phi, nest=nest)

    # Create Healpix count map
    npix = hp.nside2npix(nside)
    countmap = np.bincount(gal_hppix, weights=weights, minlength=npix)

    return countmap


# Decorate with an "accepts 1d array only" or np.vectorize?
# Or even a more specific "is healpix map" decorator?
# Or move to Python 3 and use annotations?

def hp_density_map(countmap):
    """
    Creates a Healpix density map from a number count map

    fixme-fixme-fixme
    """
    # Get mean count for non-zero pixels
    nonzero = np.take(countmap, np.where(countmap != 0))[0]
    nbar = np.mean(nonzero)

    nbarmap = nbar*np.where(countmap != 0, 1, 0)

    deltamap = countmap/nbar - 1

    return deltamap, nbarmap


if __name__ == "__main__":

    cat1 = Table.read('/home/brunomor/Work/UCL_Projects/Photoz_Cross/BOSS_data/galaxy_DR10v8_CMASS_South.fits.gz')
    cat2 = Table.read('/home/brunomor/Work/UCL_Projects/Photoz_Cross/BOSS_data/galaxy_DR10v8_CMASS_North.fits.gz')

    cat = vstack([cat1, cat2])
    

    radec = np.transpose([cat['RA'], cat['DEC']])

    nside=128
    countmap = hp_count_map(radec, nside)
    assert len(countmap) == nside*nside*12, 'bla'

    densitymap, nbarmap = hp_density_map(countmap)

    hp.write_map('counts_CMASS_N128.fits', countmap)
    hp.write_map('density_CMASS_N128.fits', densitymap)
    hp.write_map('meancounts_CMASS_N128.fits', nbarmap)

    hp.mollview(countmap, coord='GE')
    plt.show()
    hp.mollview(densitymap, coord='E')
    plt.show()
    hp.mollview(nbarmap)
    plt.show()


