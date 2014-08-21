from __future__ import division
import numpy as np
from astropy.table import Table
import os
import argparse


def main(infile, outdir):
    """
    fixme

    fixme-fixme-fixme
    """
    boss = Table.read(infile, format="fits")

    # PART 1: Restrict to official DR10 redshift range
    redshift = boss['Z']
    zrange = (redshift > 0.43) & (redshift < 0.7)
    boss = boss[zrange]

    # PART 2: Define and add w_tot column 
    # w_tot is Eq. (18) of Anderson et al. (2014) (BOSS DR10+11 paper)
    w_systot = boss['WEIGHT_SYSTOT'] # w_systot = w_seeing*w_star
    w_zf = boss['WEIGHT_NOZ']
    w_cp = boss['WEIGHT_CP']
    boss['WEIGHT_TOT'] = (w_cp + w_zf - 1)*w_systot

    # PART 3: Change name and output
    inname = os.path.basename(infile)
    name, extension = (inname[:inname.find(".fits")],
                       inname[inname.find(".fits"):])
    outname = "".join([name + "_uclvac", extension])
    outfile = os.path.join(outdir, outname)
    try:
        boss.write(outfile, format='fits')
    except IOError as err:
        raise IOError(str(err) + "\nPlease remove previous version before " +
                      "creating a new one.")

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
    parser.add_argument('-o', '--outdir',
                        default=".",
                        help="Output folder path")

    args = parser.parse_args()
    main(args.infile, args.outdir)
