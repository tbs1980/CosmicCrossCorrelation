
# A) BOSS DR10 data

For this preliminary cross-correlation exercise, we will be working with BOSS
DR10 data. The catalogs, weights and masks used can be found at the [BOSS LSS
DR10 data page](http://data.sdss3.org/sas/dr10/boss/lss/).

## A.1) Catalogs

There are several catalogs available. Most of the names are self-explanatory,
except for the ones we are going to use! These are:

   * galaxy_DR10v8_CMASS_North.fits.gz
   * galaxy_DR10v8_CMASS_South.fits.gz
   * galaxy_DR10v8_LOWZ_North.fits.gz
   * galaxy_DR10v8_LOWZ_South.fits.gz

These are catalogs of spectroscopic data from the CMASS and LOWZ samples of the
DR10 release **with accept and reject masks already applied**. A list of these
can be found in the mask section below.

## A.2) Weights

There is a series of weights that must be applied to each galaxy when
calculating clustering statistics. They are given as columns in the galaxy
catalogs. Their description and instructions on how to apply them are given in
[Anderson et al. 2012](http://mnras.oxfordjournals.org/content/427/4/3435), in
particular eq. (18):

$w_{\rm tot} = w_{\rm FKP} w_{\rm sys} (w_{\rm rf} + w_{\rm cp} -1)$

To summarize the meaning of each of these weights:

   * $w_{\rm rf}$: bla
   * $w_{\rm cp}$: bla
   * $w_{\rm sys}$: bla
   * $w_{\rm FKP}$: bla

**A point we need to discuss is which weights to use and why.** For a discussion
on how to calculate the Poisson shot noise for weighted galaxies, see Appendix A
of [Gil-Marín et al. 2014b](http://arxiv.org/abs/1407.5668).

## A.3) Completeness of sectors



## A.4) Accept and reject masks

Accept and reject masks are MANGLE polygon files with accept/reject pixels. A
detailed description of what they are and how to use them can be found in [this
tutorial](https://www.sdss3.org/dr10/tutorials/lss_galaxy.php). The masks used
in this analysis are (**cross-check this list**):

**Accept masks:**

   * mask_DR10v8_CMASS_North.ply
   * mask_DR10v8_CMASS_South.ply
   * mask_DR10v8_LOWZ_North.ply
   * mask_DR10v8_LOWZ_South.ply

These masks have a weight column that gives each sector completeness, as
described in [Anderson et al.
2012](http://mnras.oxfordjournals.org/content/427/4/3435). Each polygon belongs
to a sector, with an unique completeness value.

**Reject masks:**

   * badfield_mask_postprocess_pixs8.ply
   * badfield_mask_unphot-ugriz_pix.ply
   * bright_object_mask_rykoff_pix.ply
   * bright_star_mask.ply
   * bright_star_mask_pix.ply
   * centerpost_mask.ply
   * collision_priority_mask.ply

The masks are not needed for generating the galaxy catalogs, since there are
masked catalogs already available, but they are needed for generating a healpix
mask map. *The main task we have is to translate the information in these masks
from SDSS polygons and sectors to healpix pixels in a coherent manner.*

# B) Creating Healpix maps

...


    
