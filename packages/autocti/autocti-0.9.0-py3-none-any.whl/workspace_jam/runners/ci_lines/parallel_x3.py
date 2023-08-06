from autofit import conf
import os

# Setup the path to the workspace, using a relative directory name.
workspace_path = '{}/../../'.format(os.path.dirname(os.path.realpath(__file__)))

# Use this path to explicitly set the config path and output path.
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=workspace_path + 'output')

from autofit.tools import path_util
from autocti.data import mask as msk
from autocti.charge_injection import ci_pattern
from autocti.charge_injection import ci_data

from autocti.model import arctic_settings

from workspace_jam.tools.data_makers import tools

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

# It is convenient to specify the image type and model used to simulate that image as strings, so that if the
# pipeline is applied to multiple images we don't have to change all of the path entries in the
# load_ci_data_from_fits function below.

ci_data_type = 'ci_lines_uniform' # Charge injection data consisting of 2 images with uniform injections.
ci_data_model = 'parallel_x3' # Shows the data was creating using a parallel CTI model with one species.

# Create the path where the data will be output, which in this case is
# '/workspace/data/ci_lines_uniform/parallel_x2_species/high_res/'
ci_data_path = path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=['data', ci_data_type, ci_data_model])

# This tools loads the correct shape of the line and frame geometry, for the ci_data_resoultion string.
shape, frame_geometry = tools.charge_line_shape_and_frame_geometry_from_direction(direction='parallel')

# Specify the charge injection regions on the CCD, which in this case is 7 equally spaced rectangular blocks.
ci_regions = [(0, 30, 0, 1), (330, 360, 0, 1), (660, 690, 0, 1), (990, 1020, 0, 1),
              (1320, 1350, 0, 1), (1650, 1680, 0, 1), (1980, 2010, 0, 1)]

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
                 image_path=ci_data_path + 'line_' + str(int(normalization)) + '.fits',
                 ci_pre_cti_path=ci_data_path +'/ci_pre_cti_' + str(int(normalization)) + '.fits',
                 noise_map_from_single_value=0.1))

# The CTI settings of arCTIc, which models the CCD read-out including CTI. For parallel ci data, we include 'charge
# injection mode' which accounts for the fact that every pixel is transferred over the full CCD.
parallel_cti_settings = arctic_settings.Settings(well_depth=84700, niter=1, express=2, n_levels=2000,
                                                 charge_injection_mode=True, readout_offset=0)
cti_settings = arctic_settings.ArcticSettings(parallel=parallel_cti_settings)

def mask_function_for_bug(shape, ci_frame):
    return msk.Mask.from_masked_regions(shape=shape, masked_regions=[(0, 330, 0, 1)])

# Running a pipeline is easy, we simply import it from the pipelines folder and pass the ci data to its run function.
# Below, we'll' use a 2 phase example pipeline to fit the data with a one species parallel CTI model.
# Checkout workspace/pipelines/examples/parallel_x1_species.py' for a full description of the pipeline.

# The pool command tells our code to parallelize the analysis over 2 CPU's, where each CPU fits a different charge
# injection image

from workspace_jam.pipelines.initialize import parallel_x3

pipeline_init = parallel_x3.make_pipeline(phase_folders=[ci_data_type, ci_data_model],
                                          mask_function=mask_function_for_bug)

from workspace_jam.pipelines.normal.from_initialize import parallel_x3

pipeline_normal = parallel_x3.make_pipeline(phase_folders=[ci_data_type, ci_data_model],
                                            mask_function=mask_function_for_bug)

pipeline = pipeline_init + pipeline_normal

pipeline.run(ci_datas=datas, cti_settings=cti_settings, pool=Pool(processes=2),
             assert_optimizer_pickle_matches=False)