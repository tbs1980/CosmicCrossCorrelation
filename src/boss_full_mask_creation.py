from __future__ import division
import numpy as np
import healpy as hp
import os
import argparse


def main(accept_path, reject_paths, cboss_cut, outfolder, outfileroot):
    """
    See standalone module help for details.
    """
    # Processing accept mask
    accept_nest = hp.read_map(accept_path)
    accept_ring = hp.reorder(accept_nest, n2r=True)

    # Cutting in BOSS completeness (cf. Anderson et al. 2012) and upweighting
    accept = np.where(accept_ring >= cboss_cut, 1/accept_ring, 0)

    # Processing and merging reject masks to accept mask
    for reject_path in reject_paths:
        print os.path.basename(reject_path)
        reject_nest = hp.read_map(reject_path)
        reject_ring = hp.reorder(reject_nest, n2r=True)
        reject = np.where(reject_ring <= 0, 1, 0) # (reject = 0, all else = 1)
        accept *= reject

    # Save full mask

    mask_hires = accept # Just renaming for clarity
    n_hires = hp.get_nside(mask_hires)
    outfile = outfileroot + "_nside" + str(n_hires) + ".fits"
    outpath = os.path.join(outfolder, outfile)
    try:
        hp.write_map(outpath, mask_hires)
    except IOError:
        os.mkdir(outfolder)
        hp.write_map(outpath, mask_hires)

    # Degrade resolution down to Nside = 128 and saving

    # Set list of Nsides from 128 to original resolution
    pow2_hires = int(np.log2(n_hires))
    nsideiter = (2**i for i in range(7, pow2_hires)) # 7 --> Nside = 128

    for n in nsideiter:
        mask_lores = hp.ud_grade(mask_hires, n)
        outfile = (outfileroot + "_degraded_nside" + str(n_hires) +
                    "_to_" + str(n) + ".fits")
        outpath = os.path.join(outfolder, outfile)
        try:
            hp.write_map(outpath, mask_lores)
        except IOError:
            os.mkdir(outfolder)
            hp.write_map(outpath, mask_lores)

    return None


#--------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=
    '''
    Creates merged mask from individual BOSS healpix masks, for several Nsides.

    The goal of this standalone module is to take individual Healpix maps
    generated from BOSS original mangle masks at high resolution (i.e.
    Nside > 4096) and create a full BOSS angular selection mask. The output is
    a collection of Healpix maps, degraded from the highest resolution down to
    Nside = 128. In this case, 'degraded' means that a pixel value will be the
    average of the values at higher resolution.

    The required inputs are one BOSS accept mask and at least one reject mask.
    The accept mask has a specific format: its pixel values correspond to the
    BOSS completeness of each sector (C_BOSS, cf. Anderson et al. 2012, 2014).
    The module enforces a minimum completeness cut (cboss_cut) and the output
    mask pixels are upweighted with the accept mask '1/pixel_values'. Reject
    masks represent several excluded sectors due to bright stars, bad
    photometric conditions, etc.

    For more details on BOSS data and masks, see <put writelatex link here>.
    '''
    , fromfile_prefix_chars='@')

    parser.add_argument('--accept_path',
                        required=True,
                        help="Path to accept mask. Required.")
    parser.add_argument('--reject_paths',
                        nargs="+",
                        required=True,
                        help="Paths to reject masks. Required.")
    parser.add_argument('--cboss_cut',
                        type=float,
                        default=0.7,
                        help="BOSS completeness cut. Default: 0.7")
    parser.add_argument("--outfolder",
                        default=".",
                        help="Output folder path. Default: current dir.")
    parser.add_argument("--outfileroot",
                        default="full_mask",
                        help=("Configurable output file root name. " +
                               "Default: 'full_mask'"))

    args = parser.parse_args()
    main(args.accept_path, args.reject_paths, args.cboss_cut,
         args.outfolder, args.outfileroot)


