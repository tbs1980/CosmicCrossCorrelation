from __future__ import division
import numpy as np
import healpy as hp
import os
import sys
from functools import reduce
import operator


def process_reject_mask(reject_path):
    reject_nest = hp.read_map(reject_path)
    reject_ring = hp.reorder(reject_nest, n2r=True)
    reject = (reject_ring <= 0).astype(int)
    return reject


def merge_masks(accept_path, reject_pathlist, outfolder):
    
    masklist = map(process_reject_mask, reject_pathlist) 
    reject = reduce(operator.mul, masklist, 1)

    accept_nest = hp.read_map(accept_path)
    accept_ring = hp.reorder(accept_nest, n2r=True)
    accept = accept_ring*reject
    
    outfile = os.path.join(outfolder, infile)
    try:
        hp.write_map(outfile, accept)
    except IOError:
        os.mkdir(outfolder)
        hp.write_map(outfile, accept)
    del accept
    
    return None


if __name__ == "__main__":

    infolder = sys.argv[1]
    outfolder = sys.argv[2]

    names = ['CMASS_North', 'CMASS_South', 'LOWZ_North', 'LOWZ_South']
    nsides = ['nside' + str(2**i) for i in range(13, 14)]

    for nside in nsides:
        for name in names:
            infile = 'mask_DR10v8_' + name + '_' + nside + '_EQU.fits'
            accept_path = os.path.join(infolder, infile)
            reject_pathlist = [os.path.join(infolder, path) for path in os.listdir(infolder) if nside in path and 'DR10' not in path]
            merge_masks(accept_path, reject_pathlist, outfolder)


