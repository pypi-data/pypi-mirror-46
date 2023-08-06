from autofit import conf
from autofit.tools import path_util
from autocti.data import mask as msk
from autocti.charge_injection import ci_data
from autocti.charge_injection import ci_pattern

from autocti.model import arctic_settings

from workspace_jam.tools.data_makers import tools

from multiprocessing import Pool

import os
import sys

### NOTE - if you have not already, complete the setup in 'workspace/runners/cosma/setup' before continuing with this
### cosma pipeline script.

# Welcome to the Cosma pipeline runner. Hopefully, you're familiar with runners at this point, and have been using them
# with PyAutoCTI to model CTI on your laptop. If not, I'd recommend you get used to doing that, before trying to
# run PyAutoCTI on a super-computer. You need some familiarity with the software and before trying to model a large
# amount of charge injection imaging on a supercomputer!

# If you are ready, then let me take you through the Cosma runner. It is remarkably similar to the ordinary pipeline
# runners you're used to, however it makes a few changes for running jobs on cosma:

# 1) The data path is over-written to the path '/cosma5/data/durham/cosma_username/autocti/data' as opposed to the
#    workspace. As we saw in the setup, on cosma we don't store our data in our workspace.

# 2) The output path is over-written to the path '/cosma5/data/durham/cosma_username/autocti/output' as opposed to
#    the workspace. This is for the same reason as the data.

# Given your username is where your data is stored, you'll need to put your cosma username here.
cosma_username = 'dc-nigh1'

# The cosma path where the data and output are stored.
cosma_path = '/cosma7/data/dp004/dc-nigh1/autocti/'

# Get the relative path to the config files and output folder in our workspace.
workspace_path = '{}/../../../../'.format(os.path.dirname(os.path.realpath(__file__)))

# Use this path to explicitly set the config path, and override the output path with the Cosma path.
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=cosma_path + 'output')

# Lets take a look at a Cosma batch script, which can be found at 'workspace/runners/cosma/batch/pipeline_runner_cosma'.
# When we submit a PyAutoLens job to Cosma, we submit a 'batch' of jobs, whereby each job will run on one CPU of Cosma.
# Thus, if our lens sample contains, lets say, 4 lenses, we'd submit 4 jobs at the same time where each job applies
# our pipeline to each image.

# The fifth line of this batch script - '#SBATCH --array=1-4' is what species this. Its telling Cosma we're going to
# run 4 jobs, and the id's of those jobs will be numbered from 1 to 4. Infact, these ids are passed to this runner,
# and we'll use them to ensure that each jobs loads a different image. Lets get the cosma array id for our job.
batch_id = int(sys.argv[1])

# For a given COSMA run, we will assume all of the charge injection data-sets have identical properties. That is, they
# all have the same dimensions (shape), charge injection regions (ci_regions), charge injection normalizations
# (normalizations), charge injection patterns (patterns) and frame geometries defining the direction clocking and CTI
# (frame_geometry).

# If you need to change these value for a COSMA run, I recommend making a different runner script.

ci_data_type = 'ci_images_uniform_no_noise' # Charge injection data consisting of 2 images with uniform injections.
ci_data_model = 'serial_x3'

ci_data_resolution = []
ci_data_resolution.append('')
ci_data_resolution.append('low_resolution') # Index 1
ci_data_resolution.append('mid_resolution') # Index 2
ci_data_resolution.append('high_resolution') # Index 3

ci_data_resolution = ci_data_resolution[batch_id]

# Create the path where the data will be loaded from, which in this case is
# '/workspace/data/ci_images_uniform/serial_x2_species/high_res/'
ci_data_path = path_util.make_and_return_path_from_path_and_folder_names(
    path=cosma_path, folder_names=['data', ci_data_type, ci_data_model, ci_data_resolution])

# This tools loads the correct shape of the image and frame geometry, for the ci_data_resolution string.
shape, frame_geometry = \
    tools.serial_shape_and_frame_geometry_from_ci_data_resolution(ci_data_resolution=ci_data_resolution)

# The charge injection regions on the CCD, which in this case is 7 equally spaced rectangular blocks.
ci_regions = [(0, shape[0], 51, shape[1]-20)]

# The normalization of the charge injection for each image.
normalizations=[100.0, 500.0, 1000.0, 5000.0, 10000.0, 25000.0, 50000.0, 84700.0]

# Create the charge injection pattern objects used for this pipeline.
patterns = ci_pattern.uniform_from_lists(normalizations=normalizations, regions=ci_regions)

ci_datas = []

for index, normalization in enumerate(normalizations):

    ci_datas.append(ci_data.ci_data_from_fits(
                 frame_geometry=frame_geometry, ci_pattern=patterns[index],
                 image_path=ci_data_path + 'image_' + str(int(normalization)) + '.fits',
                 ci_pre_cti_path=ci_data_path +'ci_pre_cti_' + str(int(normalization)) + '.fits',
                 noise_map_from_single_value=0.1))

serial_cti_settings = arctic_settings.Settings(well_depth=84700, niter=1, express=2, n_levels=2000,
                                               charge_injection_mode=False, readout_offset=0)
cti_settings = arctic_settings.ArcticSettings(serial=serial_cti_settings)

# Running a pipeline is exactly the same as we're used to. We import it, make it, and run it, noting that we can
# use the lens_name's to ensure each job outputs its results to a different directory.

from workspace_jam.pipelines.initialize import serial_x3

pipeline_initialize = serial_x3.make_pipeline(phase_folders=[ci_data_type, ci_data_model, ci_data_resolution])

from workspace_jam.pipelines.normal.from_initialize import serial_x3

pipeline_normal = serial_x3.make_pipeline(phase_folders=[ci_data_type, ci_data_model, ci_data_resolution])

pipeline = pipeline_initialize + pipeline_normal

pipeline.run(ci_datas=ci_datas, cti_settings=cti_settings, pool=Pool(processes=8), assert_optimizer_pickle_matches=False)

# Finally, its worth us going through a batch script in detail, line by line, as you may we need to change different
# parts of this script to use different runners. Therefore, checkout the 'doc' file in the batch folder.