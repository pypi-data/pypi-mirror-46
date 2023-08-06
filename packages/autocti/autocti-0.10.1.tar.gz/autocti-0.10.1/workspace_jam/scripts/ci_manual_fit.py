import os

from autofit import conf
from autofit.tools import path_util
from autocti.data import mask as msk
from autocti.charge_injection import ci_pattern
from autocti.charge_injection import ci_data
from autocti.charge_injection import ci_fit

from autocti.pipeline import phase as ph
from autocti.model import arctic_params
from autocti.model import arctic_settings

from workspace_jam.tools.data_makers import tools

import numpy as np

from multiprocessing import Pool

# Welcome to the pipeline runner. This tool allows you to CTI calibration data on strong lenses, and pass it to
# pipelines for a PyAutoCTI analysis. To show you around, we'll load up some example data and run it through some of
# the example pipelines that come distributed with PyAutoCTI.

# The runner is supplied as both this Python script and a Juypter notebook. Its up to you which you use - I personally
# prefer the python script as provided you keep it relatively small, its quick and easy to comment out data-set names
# and pipelines to perform different analyses. However, notebooks are a tidier way to manage visualization - so
# feel free to use notebooks. Or, use both for a bit, and decide your favourite!

# The pipeline runner is fairly self explanatory. Make sure to checkout the pipelines in the
#  workspace/pipelines/examples/ folder - they come with detailed descriptions of what they do. I hope that you'll
# expand on them for your own personal scientific needs

# Setup the path to the workspace, using a relative directory name.
workspace_path = '{}/../'.format(os.path.dirname(os.path.realpath(__file__)))

# Use this path to explicitly set the config path and output path.
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=workspace_path + 'output')

# It is convenient to specify the image type and model used to simulate that image as strings, so that if the
# pipeline is applied to multiple images we don't have to change all of the path entries in the
# load_ci_data_from_fits function below.

ci_data_type = 'ci_images_uniform_no_noise' # Charge injection data consisting of 2 images with uniform injections.
ci_data_model = 'serial_x3' # Shows the data was creating using a serial CTI model with one species.
ci_data_resolution = 'low_resolution' # The resolution of the image.

# Create the path where the data will be loaded from, which in this case is
# '/workspace/data/ci_images_uniform/serial_x3_species/high_res/'
ci_data_path = path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=['data', ci_data_type, ci_data_model, ci_data_resolution])

# This tools loads the correct shape of the image and frame geometry, for the ci_data_resolution string.
shape, frame_geometry = \
    tools.serial_shape_and_frame_geometry_from_ci_data_resolution(ci_data_resolution=ci_data_resolution)

# The charge injection regions on the CCD, which in this case is 7 equally spaced rectangular blocks.
ci_regions = [(0, shape[0], 51, shape[1]-20)]

# The normalization of the charge injection for each image.
normalizations=[100.0, 500.0, 1000.0, 5000.0, 10000.0, 25000.0, 50000.0, 84700.0]

# Create the charge injection pattern objects used for this pipeline.
patterns = ci_pattern.uniform_from_lists(normalizations=normalizations, regions=ci_regions)

# There are 8 images to load, which is what the normalizations list tells us. To load them, its easiest to create a
# 'data' list and then iterate over a for loop, to append each set of data to the list of data we pass to the pipeline
# when we run it.

datas = []

for index, normalization in enumerate(normalizations):

    datas.append(ci_data.ci_data_from_fits(
                 frame_geometry=frame_geometry, ci_pattern=patterns[index],
                 image_path=ci_data_path + 'image_' + str(int(normalization)) + '.fits',
                 ci_pre_cti_path=ci_data_path +'/ci_pre_cti_' + str(int(normalization)) + '.fits',
                 noise_map_from_single_value=4.0))

# The CTI settings of arCTIc, which models the CCD read-out including CTI. For serial ci data, we include 'charge
# injection mode' which accounts for the fact that every pixel is transferred over the full CCD.
serial_cti_settings = arctic_settings.Settings(well_depth=84700, niter=1, express=2, n_levels=2000,
                                        charge_injection_mode=False, readout_offset=0)
cti_settings = arctic_settings.ArcticSettings(serial=serial_cti_settings)

serial_species_0 = arctic_params.Species(trap_density=0.01, trap_lifetime=0.8)
serial_species_1 = arctic_params.Species(trap_density=0.03, trap_lifetime=4.0)
serial_species_2 = arctic_params.Species(trap_density=0.9, trap_lifetime=20.0)

serial_ccd = arctic_params.CCD(well_notch_depth=1.0e-4, well_fill_alpha=1.0, well_fill_beta=0.58)
cti_params = arctic_params.ArcticParams(serial_species=[serial_species_0, serial_species_1, serial_species_2],
                                        serial_ccd=serial_ccd)


mask_function=msk.Mask.empty_for_shape
masks = list(map(lambda data: mask_function(shape=data.image.shape), datas))
phase = ph.SerialPhase(rows=(0, 10), phase_name='test')
ci_datas_fit = [phase.extract_ci_data(data=data, mask=mask) for data, mask in zip(datas, masks)]

fits = list(map(lambda ci_data_fit:
                ci_fit.CIFit(masked_ci_data=ci_data_fit, cti_params=cti_params, cti_settings=cti_settings),
                ci_datas_fit))

print(list(map(lambda fit : np.max(fit.residual_map), fits)))
print(list(map(lambda fit : fit.likelihood, fits)))