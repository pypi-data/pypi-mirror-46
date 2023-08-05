from autofit import conf
from autofit.tools import path_util
from autolens.data import ccd
from autolens.data.array import mask as msk
from autolens.model.profiles import light_profiles as lp
from autolens.model.profiles import mass_profiles as mp
from autolens.model.galaxy import galaxy as g
from autolens.lens import ray_tracing
from autolens.lens import lens_fit
from autolens.lens import lens_data as ld
from autolens.lens import plane as pl
from autolens.model.inversion import inversions as inv
from autolens.model.inversion import pixelizations as pix
from autolens.model.inversion import regularization as reg
from autolens.lens.plotters import lens_fit_plotters

import os

workspace_path = '{}/../'.format(os.path.dirname(os.path.realpath(__file__)))
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=workspace_path + 'output/subhalo_challenge/')

data_type = 'noise_10'
data_level = 'level_1'
data_name = 'large_hi_sn_system_1'

pixel_scale = 0.00976562

data_path = path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=['data', 'subhalo_challenge', data_type, data_level, data_name])

resized_shape = (700, 700)

ccd_data = ccd.load_ccd_data_from_fits(image_path=data_path + 'image.fits',
                                       psf_path=data_path + 'psf.fits',
                                       noise_map_path=data_path + 'noise_map.fits',
                                       pixel_scale=pixel_scale, resized_ccd_shape=resized_shape, resized_psf_shape=(9, 9))

mask = msk.load_mask_from_fits(mask_path=data_path + 'mask_irregular.fits', pixel_scale=pixel_scale)
mask = mask.resized_scaled_array_from_array(new_shape=resized_shape)


# The lines of code below do everything we're used to, that is, setup an image and its grid stack, mask it, trace it
# via a tracer, setup the rectangular mapper, etc.
lens_galaxy = g.Galaxy(mass=mp.EllipticalIsothermal(centre=(0.002, 0.003), axis_ratio=0.138, phi=5.83,
                                                    einstein_radius=1.84),
                       shear=mp.ExternalShear(magnitude=0.12, phi=91.2))

lens_data = ld.LensData(ccd_data=ccd_data, mask=mask)

adaptive = pix.AdaptiveMagnification(shape=(30, 30))

# Now lets plot our rectangular mapper with the image.
# mapper_plotters.plot_image_and_mapper(ccd_data=ccd_data, mapper=mapper, mask=mask, should_plot_grid=True)

# Okay, so lets think about the rectangular pixelization. Is it the optimal way to pixelize our source plane? Are there
# features in the source-plane that arn't ideal? How do you think we could do a better job?

# Well, given we're doing a whole tutorial on using a different pixelization to the rectangular grid, you've probably
# guessed that it isn't optimal. Infact, its pretty rubbish, and not a pixelization we'll actually want to model
# many lenses with!

# So what is wrong with the grid? Well, first, lets think about the source reconstruction.
# inversion_plotters.plot_reconstructed_pixelization(inversion=inversion, should_plot_centres=True)

source_galaxy = g.Galaxy(pixelization=adaptive, regularization=reg.Constant(coefficients=(1.0,)))
tracer = ray_tracing.TracerImageSourcePlanes(lens_galaxies=[lens_galaxy], source_galaxies=[source_galaxy],
                                             image_plane_grid_stack=lens_data.grid_stack)
fit = lens_fit.LensDataFit.for_data_and_tracer(lens_data=lens_data, tracer=tracer)

lens_fit_plotters.plot_fit_subplot(fit=fit, should_plot_mask=True, extract_array_from_mask=True, zoom_around_mask=True)