from __future__ import division
import numpy as np
import healpy as hp
from astropy.table import Table
import os
import argparse
import ast


def apply_cuts(data, **kwargs):
    """
    fixme

    fixme-fixme-fixme
    """
    mask = np.ones(len(data), dtype=bool)
    
    for field, cuts in kwargs.items():
        fieldmask = np.zeros(len(data), dtype=bool)
        try:
            for low, upp in cuts:
                if low is None:
                    low = '-inf'
                if upp is None:
                    upp = 'inf'
                fieldmask = fieldmask | ( (data[field] >= float(low)) &
                                          (data[field] < float(upp)) )
        except TypeError:
            raise TypeError(field + " values must be a 2d tuple or list of " +
                        "numbers (int or float) or None.")
        except ValueError:
            raise ValueError(field + "values must be a 2d tuple or list of " +
                        "numbers (int or float) or None.")
        except KeyError:
            raise KeyError("At least one of the fields is not present " +
                       "in the catalog.")
        mask = mask & fieldmask

    newdata = data[mask]

    return newdata


def bin_data(data, field, binlist):
    """
    fixme

    fixme-fixme-fixme
    """
    bincol = data[field]
    masks = ((bincol >= inf) & (bincol < sup) for (inf, sup) in binlist)
    datalist = [data[mask] for mask in masks]

    return datalist


def hp_count_map(radecdata, nside, weights=None, nest=False):
    """
    Creates a Healpix object count map from a 2d array of RA, DEC positions

    fixme-fixme-fixme
    """

    # Sanity checks
    if weights is not None:
        assert len(weights) == len(radecdata), ("Weights and data must have " +
                                                "the same length")
    assert hp.isnsideok(nside), "nside must be a power of 2"

    # Assign each galaxy to a Healpix pixel
    deg2rad = np.pi/180
    theta = deg2rad*(90.0 - radecdata[:, 1])
    phi = deg2rad*radecdata[:, 0]
    gal_hppix = hp.ang2pix(nside, theta=theta, phi=phi, nest=nest)

    # Create Healpix count map
    npix = hp.nside2npix(nside)
    countmap = np.bincount(gal_hppix, weights=weights, minlength=npix)

    return countmap


def main(infile, nside, raname, decname, wname, zname, zbins, cuts, outdir):
    """
    fixme

    fixme-fixme-fixme
    """

    data = Table.read(infile, format="fits")

    # Input sanity checks
    colnames = data.columns
    assert (raname in colnames) and (decname in colnames), ("Both ra " +
                              "and dec names must exist in the catalog.")
    if wname is not None:
        assert wname in colnames, ("If you're using a weight column, " +
                                                   "select correct name")
    if cuts is not None:
        data = apply_cuts(data, **cuts)

    # Redshift binning
    if (zname is not None) and (zbins is not None):
        datalist = bin_data(data, zname, zbins)
        zsuffix = ["_z%.2f-%.2f" % (inf, sup) for (inf, sup) in zbins]
    else:
        print "For redshift binning, both zname and zbins must be given."
        print "Proceeding without binning."
        datalist = [data]
        zsuffix = [""]

    # Create maps for all bins
    for (newdata, zname) in zip(datalist, zsuffix):
        # Select fields
        radec = np.transpose([newdata[raname].data, newdata[decname].data])
        if wname is not None:
            weight = newdata[wname].data
        else:
            weight = None

        # Create weighted count maps
        weighted_counts = hp_count_map(radec, nside, weights=weight)

        # Define output names
        try:
            os.mkdir(outdir)
        except OSError:
            if not os.path.isdir(outdir):
                raise

        suffix = "_N" + str(nside) + zname
        outcounts = os.path.join(outdir, "weighted_counts" + suffix +".fits")

        # Save outputs
        hp.write_map(outcounts, weighted_counts)

    return None


#--------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=
    '''
    fixme

    fixme - fixme - fixme
    '''
    , fromfile_prefix_chars='@')

    parser.add_argument('infile',
                        help="Path to input data")
    parser.add_argument('--nside',
                        type=int,
                        default=128,
                        required=True,
                        help="Healpix output map resolution")
    parser.add_argument('--raname',
                        default='RA',
                        required=True,
                        help="RA field name")
    parser.add_argument('--decname',
                        default='DEC',
                        required=True,
                        help="DEC field name")
    parser.add_argument('--wname',
                        default=None,
                        help="Weight field name, where applicable")
    parser.add_argument('--zname',
                        default=None,
                        help="Redshift field name, where applicable")
    parser.add_argument('--zbins',
                        type=ast.literal_eval,
                        default=None,
                        help=("List of bins. Format should be " +
                              "[(b1inf, b1sup), ..., (bNinf, bNsup)]"))
    parser.add_argument('-c', '--cuts',
                        type=ast.literal_eval,
                        default=None,
                        help=("Dictionary of cuts. Format should be " +
                              "{'k1:(v1inf,v1sup)',...,'kN:(vNinf,vNsup)'}"))
    parser.add_argument("-o", "--outdir",
                        default=".",
                        help="Output folder path")

    args = parser.parse_args()
    main(args.infile, args.nside, args.raname, args.decname, args.wname,
         args.zname, args.zbins, args.cuts, args.outdir)
