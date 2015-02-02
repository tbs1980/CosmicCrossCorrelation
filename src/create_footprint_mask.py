from __future__ import division, print_function
import numpy as np
import healpy as hp
import os
import argparse
import ast
import errno


def main(masklist, degrade, outfolder, outfileroot):
    """
    For help, type 'python create_footprint_mask.py -h'.
    """
    maplist = []
    nsidelist = []

    # 1) Operating on individual masks
    for mask in masklist:
        path = mask['path']
        cut = mask['cut']
        invert = mask['invert']
        unseen = mask['unseen']

        hpmap = hp.read_map(path)
        nside = hp.get_nside(hpmap)
        nsidelist.append(nside)
        hp_seen = (hpmap != hp.UNSEEN)

        if cut is not None:
            hpmap = np.where((hpmap < cut) & hp_seen, 1, 0)
        else:
            assert np.all((hpmap[hp_seen] == 0) | (hpmap[hp_seen] == 1)), (""+
                  "If there is no cut, the map must consist of zeros and ones")
        if invert:
            hpmap[hp_seen] = np.where((hpmap[hp_seen] == 1), 0, 1)
        if unseen is not None:
            hpmap[~hp_seen] = unseen

        maplist.append(hpmap)
        del hpmap, nside

    # 2) Upgrading to common high resolution and merging
    n_hires = max(nsidelist)
    mask_hires = np.ones(hp.nside2npix(n_hires))
    for hpmap, nside in zip(maplist, nsidelist):
        if nside < n_hires:
            hpmap = hp.ud_grade(hpmap, n_hires)
        mask_hires *= hpmap
        del hpmap

    # 3) Save full mask
    try:
        os.makedirs(outfolder)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    outfile = outfileroot + "_nside" + str(n_hires) + ".fits"
    outpath = os.path.join(outfolder, outfile)
    hp.write_map(outpath, mask_hires)

    # 4) Degrade resolution down to Nside = 128 and saving
    if degrade:
        pow2_hires = int(np.log2(n_hires))
        nsideiter = (2**i for i in xrange(7, pow2_hires)) # 7 --> Nside = 128
        for nside in nsideiter:
            mask_lores = hp.ud_grade(mask_hires, nside)
            outfile = (outfileroot + "_degraded_nside" + str(n_hires) +
                       "_to_" + str(nside) + ".fits")
            outpath = os.path.join(outfolder, outfile)
            hp.write_map(outpath, mask_lores)
            del mask_lores

    return None

#--------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=
    '''
    Creates merged footprint mask from individual healpix maps.

    The goal of this standalone module is to take individual Healpix maps
    and create a full footprint angular selection mask. The output is either a
    Healpix 0/1 map of same resolution as the highest resolution input map or,
    if the option --degrade is used, a collection of Healpix maps degraded from
    the highest resolution down to Nside = 128. In this case, 'degraded' means
    that a pixel value will be the average of the values at higher resolution.

    The input masks are given as dictionaries, with 'path', 'invert', 'cut' and
    'unseen' keys. The three latter keys correspond to the following
    implemented operations:

        - 'invert' (boolean): transform a 0/1 mask to 1/0 before merging.
        - 'cut' (None or float): if it is a float mask, a pixvalue < cut is
          applied to create a 0/1 mask. If the user wants a >= cut, combine
          'cut' and 'invert' keys. If he/she wants both a < and >= cut, use two
          dictionaries for the same mask, one for each cut.
        - 'unseen' (None or float): chooses values for Healpix masked
          pixels. If None, it will leave default Healpix value for masks (i.e.
          -1.6735e30. If a float value is chosen, masked pixels will be set to
          this value before saving. None of the operations in the pipeline are
          performed on these pixels, other than setting this value.)

    It is suggested that the user works with a config file for the input, with
    one python dictionary per mask per line under the option --masks. Example:

    --masks
    {'path': '/path/to/mask1.fits', 'invert': False, 'cut': None, 'unseen': 0}
    {'path': '/path/to/mask2.fits', 'invert': True, 'cut': 0.7, 'unseen': None}
    ...

    The command-line call is 'python create_footprint_mask.py @/path/to/cfgfile'
    '''
    , fromfile_prefix_chars='@')

    parser.add_argument('--masks',
                        nargs="+",
                        type=ast.literal_eval,
                        required=True,
                        help=("List of dictionaries with mask properties " +
                              "(path, invert, cut, unseens)"))
    parser.add_argument('--degrade',
                        action='store_true',
                        default=False,
                        help="Create masks with degraded Nside. Default:False")
    parser.add_argument("--outfolder",
                        default=".",
                        help="Output folder path. Default: current dir.")
    parser.add_argument("--outfileroot",
                        default="full_mask",
                        help=("Configurable output file root name. " +
                               "Default: 'full_mask'"))

    args = parser.parse_args()
    main(args.masks, args.degrade, args.outfolder, args.outfileroot)
