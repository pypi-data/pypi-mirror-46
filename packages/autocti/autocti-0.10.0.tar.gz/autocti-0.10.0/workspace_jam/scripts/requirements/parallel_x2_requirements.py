from autofit import conf
from autofit import aggregator
from autocti.model import arctic_params as ap
import os
import numpy as np

from workspace_jam.scripts.requirements.tools import weighted_avg_and_std

def parallel_x2_requirements_of_resolutions(ci_resolutions):

    # Setup the path to the workspace, using a relative directory name.
    workspace_path = '{}/../../'.format(os.path.dirname(os.path.realpath(__file__)))
    output_path = workspace_path + '../../outputs/PyAutoCTI/'

    # Use this path to explicitly set the config path and output path.
    conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=output_path)

    input_parallel_species_0 = ap.Species(trap_density=0.13, trap_lifetime=1.25)
    input_parallel_species_1 = ap.Species(trap_density=0.25, trap_lifetime=4.4)
    input_arctic_params = ap.ArcticParams(parallel_species=[input_parallel_species_0, input_parallel_species_1])
    input_delta_ellipticity = input_arctic_params.delta_ellipticity

    pipeline = 'pipeline_normal__parallel_x2'
    phase = 'phase_1_parallel_x2'

    ci_image = 'ci_images_non_uniform_cosmic_rays'
    ci_model = 'parallel_x2_poisson'
    ci_setting = 'settings_cr_p10s10d3'

    requirement_means_of_resolutions = []
    requirement_stds_of_resolutions = []
    requirement_errors_of_resolutions= []

    for ci_resolution in ci_resolutions:

        agg = aggregator.Aggregator(directory=output_path + ci_image + '/' + ci_model + '/' + ci_resolution + '/' + pipeline + '/' + phase + '/' + ci_setting)
        optimizer = agg.optimizers_with(pipeline=pipeline, phase=phase)[0]

        weights = []
        requirements = []

        for sample_index in range(optimizer.total_samples):

            weight = optimizer.sample_weight_from_sample_index(sample_index=sample_index)

            if weight > 1.0e-4:

                params = optimizer.sample_model_parameters_from_sample_index(sample_index=sample_index)
                params.append(0.0)
                params.append(0.0)
                params[1], params[2] = params[2], params[1]
                instance = optimizer.variable.instance_from_physical_vector(physical_vector=params)
        #        print(instance.parallel_species[0].trap_density)
        #        print(instance.parallel_species[1].trap_density)
        #        print(instance.parallel_species[0].trap_lifetime)
        #        print(instance.parallel_species[1].trap_lifetime)
        #        instance = optimizer.sample_model_instance_from_sample_index(sample_index=sample_index)
                params = ap.ArcticParams(parallel_species=instance.parallel_species)
                requirement = (params.delta_ellipticity - input_delta_ellipticity) / 1.1e-4
                weights.append(weight)
                requirements.append(requirement)

        requirement_mean, requirement_std = weighted_avg_and_std(values=requirements, weights=weights)

        requirement_means_of_resolutions.append(requirement_mean)
        requirement_stds_of_resolutions.append(requirement_std)
        requirement_errors_of_resolutions.append(requirement_std / 2.0)

    return requirement_means_of_resolutions, requirement_errors_of_resolutions
