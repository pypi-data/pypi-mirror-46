from autofit import conf
from autofit import aggregator
import os

# Setup the path to the workspace, using a relative directory name.
workspace_path = '{}/../'.format(os.path.dirname(os.path.realpath(__file__)))

# Use this path to explicitly set the config path and output path.
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=workspace_path + 'output')

pipeline = 'pipeline_init__parallel_x2 + pipeline_normal__parallel_x2'
phase = 'phase_1_parallel_x2'



agg = aggregator.Aggregator(directory=workspace_path + 'output/ci_images_uniform/parallel_x2/high_resolution/')

opt = agg.optimizers_with(pipeline=pipeline, phase=phase)

print(opt)