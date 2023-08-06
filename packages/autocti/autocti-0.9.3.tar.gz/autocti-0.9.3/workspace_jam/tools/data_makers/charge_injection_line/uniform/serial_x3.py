from autofit.tools import path_util
from autocti.charge_injection import ci_data
from autocti.charge_injection import ci_pattern
from autocti.data import util

from autocti.model import arctic_settings
from autocti.model import arctic_params

from workspace_jam.tools.data_makers import tools

import os

# This tool allows one to make simulated charge injection imaging data-sets for calibrating parallel charge transfer
# inefficiency, which can be used to test example pipelines and investigate CTI modeling on data-sets where the
# 'true' answer is known.

# The 'ci_data_type', 'ci_data_model' and 'ci_data_resolution' determine the directory the output data folder, e.g:

# The line will be output as '/workspace/data/ci_data_type/ci_data_model/ci_data_resolution/ci_line.fits'.
# The noise-map will be output as '/workspace/data/ci_data_type/ci_data_model/ci_data_resolution/ci_noise_map.fits'.
# The pre cti ci line will be output as '/workspace/data/ci_data_type/ci_data_model/ci_data_resolution/ci_pre_cti.fits'.

# Lets setup the relative path to the workspace, so we can output the data in the 'data' folder..
workspace_path = '{}/../../../../'.format(os.path.dirname(os.path.realpath(__file__)))

ci_data_type = 'ci_lines_uniform'
ci_data_model = 'serial_x3'

# Create the path where the data will be output, which in this case is
# '/workspace/data/ci_lines_uniform/parallel_x2_species/high_res/'
ci_data_path = path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=['data', ci_data_type, ci_data_model])

# This tools loads the correct shape of the line and frame geometry, for the ci_data_resoultion string.
shape, frame_geometry = tools.charge_line_shape_and_frame_geometry_from_direction(direction='serial')

# Specify the charge injection regions on the CCD, which in this case is 7 equally spaced rectangular blocks.
ci_regions = [(0, 1, 51, shape[1]-20)]

# The normalization of every ci line - this size of this list thus determines how many lines are simulated.
normalizations=[100.0, 500.0, 1000.0, 5000.0, 10000.0, 25000.0, 50000.0, 84700.0]

# The CTI settings of arCTIc, which models the CCD read-out including CTI. For serial ci data, we include 'charge
# injection mode' which accounts for the fact that every pixel is transferred over the full CCD.
serial_cti_settings = arctic_settings.Settings(well_depth=84700, niter=1, express=2, n_levels=2000,
                                               charge_injection_mode=False, readout_offset=0)
cti_settings = arctic_settings.ArcticSettings(serial=serial_cti_settings)

# The CTI model parameters of arCTIc, which includes each trap species density / lifetime and the CCD properties for
# serial charge transfer.
serial_species_0 = arctic_params.Species(trap_density=0.01, trap_lifetime=0.8)
serial_species_1 = arctic_params.Species(trap_density=0.03, trap_lifetime=4.0)
serial_species_2 = arctic_params.Species(trap_density=0.9, trap_lifetime=20.0)

serial_ccd = arctic_params.CCD(well_notch_depth=1.0e-4, well_fill_alpha=1.0, well_fill_beta=0.58)
cti_params = arctic_params.ArcticParams(serial_species=[serial_species_0, serial_species_1, serial_species_2],
                                        serial_ccd=serial_ccd)

# Use the ci normalizations and regions to create the ci pattern of every line that is to be simulated.

# This function creates uniform blocks of charge injection lines, given an input normalization and list of regions.
ci_patterns = ci_pattern.uniform_from_lists(normalizations=normalizations, regions=ci_regions)

# Use the simulate ci patterns to generate the pre-cti charge injection lines.
ci_pre_ctis = list(map(lambda ci_pattern :
                       ci_pattern.simulate_ci_pre_cti(shape=shape),
                       ci_patterns))

# Use every ci pattern to simulate a ci line.
datas = list(map(lambda ci_pre_cti, ci_pattern:
                    ci_data.simulate(ci_pre_cti=ci_pre_cti, frame_geometry=frame_geometry,
                                      ci_pattern=ci_pattern, cti_settings=cti_settings, cti_params=cti_params,
                                      read_noise=None),
                 ci_pre_ctis, ci_patterns))

# Now, output every line to the data folder as the filename 'ci_data_normalization.fits'
list(map(lambda ci_data, normalization :
         util.numpy_array_2d_to_fits(array_2d=ci_data.image,
                                     file_path=ci_data_path + 'line_' + str(int(normalization)) + '.fits',
                                     overwrite=True),
         datas, normalizations))

# Output every pre-cti line to the data folder as the filename 'ci_pre_cti_normalization.fits'. This allows the
# calibration pipeline to load these lines as the model pre-cti lines, which is necessary for non-uniform ci patterns.
list(map(lambda ci_data, normalization :
         util.numpy_array_2d_to_fits(array_2d=ci_data.ci_pre_cti,
                                     file_path=ci_data_path + 'ci_pre_cti_' + str(int(normalization)) + '.fits',
                                     overwrite=True),
         datas, normalizations))