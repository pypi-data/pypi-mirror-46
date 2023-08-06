from autofit import conf
from autofit import aggregator
import os
import numpy as np
import matplotlib.pyplot as plt

# Setup the path to the workspace, using a relative directory name.
workspace_path = '{}/../../'.format(os.path.dirname(os.path.realpath(__file__)))
plot_path = '{}/plotting/results/plots/'.format(workspace_path)
output_path = workspace_path + '../../outputs/PyAutoCTI/'

# Use this path to explicitly set the config path and output path.
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=output_path)

pipeline = 'pipeline_normal__parallel_x2'
phase = 'phase_1_parallel_x2'

sigma_limit = 2.0

ci_image = 'ci_images_non_uniform_cosmic_rays'
ci_model = 'parallel_x2_poisson'
ci_setting = 'settings_cr_p10s10d3'
ci_resolution = 'high_resolution'

total_params = 6

agg = aggregator.Aggregator(directory=output_path + ci_image + '/' + ci_model + '/' + ci_resolution + '/' + pipeline + '/' + phase + '/' + ci_setting)
optimizer = agg.optimizers_with(pipeline=pipeline, phase=phase)[0]

most_probable = optimizer.most_probable_model_parameters
most_probable.pop(7)
most_probable.pop(6)
model_errors = optimizer.model_errors_at_sigma_limit(sigma_limit=sigma_limit)

# Trap Density 1 -> 0.84 +- 0.33 %
# Trap Density 2 -> 0.39 +- 0.06 %
# Trap Density 3 -> 0.0303 +- 0.0007 %
# Trap Release 1 -> 1.93 +- 0.23 %
# Trap Release 2 -> 3.0 +- 3.6 %
# Trap Release 3 -> 0.0400 +- 0.0004 %
# Beta -> 0.0000631 (absolute terms)

print('Percentages:')
print(list(map(lambda mp, error : 100*np.abs(error / mp), most_probable, model_errors)), '\n')

print(most_probable)
print(model_errors)

print('Beta From Israel = ', model_errors[5] / 0.0000631)