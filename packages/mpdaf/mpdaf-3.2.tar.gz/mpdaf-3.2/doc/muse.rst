************************************
MUSE specific tools (``mpdaf.MUSE``)
************************************

Python interface for MUSE slicer numbering scheme
=================================================

The `~mpdaf.MUSE.Slicer` class contains a set of static methods to convert
a slice number between the various numbering schemes. The definition of the
various numbering schemes and the conversion table can be found in the *“Global
Positioning System”* document (VLT-TRE-MUSE-14670-0657).

All the methods are static and thus there is no need to instantiate an object
to use this class.

For example, we convert slice number 4 in CCD numbering to SKY numbering:

.. ipython::

  In [1]: from mpdaf.MUSE import Slicer

  In [2]: Slicer.ccd2sky(4)

Now we convert slice number 12 of stack 3 in OPTICAL numbering to CCD numbering:

.. ipython::

  In [3]: Slicer.optical2sky((2, 12))

MUSE LSF models
===============

.. warning:: LSF class is currently under development

Only one model of LSF (Line Spread Function) is currently available.

LSF *qsim_v1*
-------------

This is a simple model where the LSF is supposed to be constant over the filed
of view. It uses a simple parametric model of variation with wavelength.

The model is a convolution of a step function with a Gaussian. The resulting
function is then sample by the pixel size::

    LSF = T(y2+dy/2) - T(y2-dy/2) - T(y1+dy/2) + T(y1-dy/2)

    T(x) = exp(-x**2/2) + sqrt(2*pi)*x*erf(x/sqrt(2))/2

    y1 = (y-h/2) / sigma

    y2 = (y+h/2) / sigma

The slit width is assumed to be constant (h = 2.09 pixels).  The Gaussian sigma
parameter is a polynomial approximation of order 3 with wavelength::

    c = [-0.09876662, 0.44410609, -0.03166038, 0.46285363]

    sigma(x) = c[3] + c[2]*x + c[1]*x**2 + c[0]*x**3


To use it, create a `~mpdaf.MUSE.LSF` object with attribute 'typ' equal to
'qsim_v1':

.. ipython::

  In [1]: from mpdaf.MUSE import LSF

  In [2]: lsf = LSF(typ='qsim_v1')

Then get the LSF array by using `~mpdaf.MUSE.LSF.get_LSF`:

.. ipython::

  In [3]: lsf_6000 = lsf.get_LSF(lbda=6000, step=1.25, size=11)

  In [4]: import matplotlib.pyplot as plt

  In [5]: import numpy as np

  @savefig simple_LSF.png width=4in
  In [6]: plt.plot(np.arange(-5,6), lsf_6000, drawstyle='steps-mid')


MUSE FSF models
===============

.. warning:: FSF class is currently under development

Two models of FSF (Field Spread Function) are currently available:

- `~mpdaf.MUSE.OldMoffatModel` (``model='MOFFAT1'``): the old model with a fixed
  beta.

- `~mpdaf.MUSE.MoffatModel2` (``model=2``): a circular MOFFAT with polynomials
  for beta and FWHM.

Example with *MOFFAT1*
----------------------

The MUSE FSF is supposed to be a Moffat function with a FWHM which varies
linearly with the wavelength:

    :math:`FWHM = a + b * lbda`

With:

 - beta (float) Power index of the Moffat.
 - a (float) constant in arcsec which defined the FWHM.
 - b (float) constant which defined the FWHM.

We create the `~mpdaf.MUSE.FSFModel` object like this:

.. ipython::

  In [1]: from mpdaf.MUSE import FSFModel, OldMoffatModel

  In [2]: fsf = OldMoffatModel(a=0.885, b=-2.94E-05, beta=2.8, pixstep=0.2)

  In [3]: isinstance(fsf, FSFModel)

Various methods allow to get the FSF array (2D or 3D, as mpdaf Image or Cube)
for given wavelengths, or the FWHM in pixel and in arcseconds.

.. ipython::

  In [1]: lbda = np.array([5000, 9000])

  In [4]: fsf.get_fwhm(lbda)

  In [5]: fsf.get_fwhm(lbda, unit='pix')

  In [20]: im5000 = fsf.get_2darray(lbda[0], shape=(25, 25))

  In [20]: fsfcube = fsf.get_3darray(lbda, shape=(25, 25))

  In [27]: plt.figure()

  @savefig FSF1.png width=3.5in
  In [26]: plt.imshow(im5000)

  In [27]: plt.figure()

  @savefig FSF2.png width=3.5in
  In [28]: plt.imshow(fsfcube[1])

The FSF model can be saved to a FITS header with
`mpdaf.MUSE.FSFModel.to_header`, and read with `mpdaf.MUSE.FSFModel.read`.


MUSE mosaic field map
=====================

.. warning:: FieldsMap class is currently under development

`~mpdaf.MUSE.FieldsMap` reads the possible FIELDMAP extension of the MUSE data
cube.

.. ipython::

  In [1]: from mpdaf.MUSE import FieldsMap

  In [7]: fmap = FieldsMap('sdetect/subcub_mosaic.fits', extname='FIELDMAP')

`~mpdaf.MUSE.FieldsMap.get_pixel_fields` returns a list of fields that cover
a given pixel (y, x):

.. ipython::

  In [23]: fmap.get_pixel_fields(0,0)

  In [20]: fmap.get_pixel_fields(20,20)

`~mpdaf.MUSE.FieldsMap.get_field_mask` returns an array with non-zeros values
for pixels matching a field:

.. ipython::

  In [14]: plt.figure()

  @savefig fmap1.png width=3.5in
  In [15]: plt.imshow(fmap.get_field_mask('UDF-06'), vmin=0, vmax=1)

  In [14]: plt.figure()

  @savefig fmap2.png width=3.5in
  In [13]: plt.imshow(fmap.get_field_mask('UDF-09'), vmin=0, vmax=1)


Reference/API
=============

.. automodapi:: mpdaf.MUSE
   :no-main-docstr:

.. ipython::
   :suppress:

   In [4]: plt.close("all")

   In [4]: %reset -f
