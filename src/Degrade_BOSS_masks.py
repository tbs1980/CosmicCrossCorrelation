from __future__ import division
import numpy as np
import healpy as hp
import os

infile = sys.argv[1]
outfolder = sys.argv[2]

# Open high resolution mask
mask_hifi = hp.read_map(infile)

n_hifi = hp.get_nside(mask_hifi)
pow2_hifi = int(np.log2(n_hifi))
nsideiter = (2**i for i in range(7, pow2_hifi)) # 7 --> Nside = 128

for i in nsideiter:
    mask_lofi = hp.ud_grade(mask_hifi, i)
    outfile = os.path.join(outfolder, "full_mask_degraded_" + str(n_hifi) + "_to_" + str(i) + ".fits")
    try:
        hp.write_map(outfile, mask_lofi)
    except IOError:
        os.mkdir(outfolder)
        hp.write_map(outfile, mask_lofi)



