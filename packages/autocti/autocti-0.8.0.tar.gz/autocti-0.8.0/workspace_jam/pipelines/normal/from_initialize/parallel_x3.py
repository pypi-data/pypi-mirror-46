from autofit.tools import path_util
from autofit.optimize import non_linear as nl
from autofit.mapper import prior
from autofit.mapper import prior_model
from autocti.data import mask as msk
from autocti.pipeline import pipeline as pl
from autocti.pipeline import phase as ph
from autocti.model import arctic_params

# In this pipeline, we'll perform an analysis which fits three parallel trap species to a set of charge
# injection imaging data. This will include a hyper-phase which scales the noise in the analysis, to prevent
# over-fitting the highest S/N charge injection images. The pipeline uses four phases:

# Phase 1) Fit a small section (60 columns of every charge injection) using a parallel CTI model
#          with 1 trap species and a model for the parallel CCD volume filling parameters.

# Phase 2) Fit a small section (again, 60 columns) using a parallel CTI model with 3 trap species and a model for the
#          parallel CCD volume filling parameters. The priors on trap densities and volume filling parameters are
#          initialized from the results of phase 1.

# Phase 3) Use the best-fit model from phase 2 to scale the noise of each image, to ensure that the higher and
#          lower S/N images are weighted more equally in their contribution to the likelihood.

# Phase 4) Refit the phase 2 model, using priors initialized from the results of phase 2 and the scaled noise-map
#          computed in phase 3.

def make_pipeline(phase_folders=None, tag_phases=True, mask_function=msk.Mask.empty_for_shape,
                  parallel_front_edge_mask_rows=None, parallel_trails_mask_rows=None,
                  parallel_total_density_range=None,
                  cosmic_ray_parallel_buffer=None, cosmic_ray_serial_buffer=None, cosmic_ray_diagonal_buffer=None):

    pipeline_name = 'pipeline_normal__parallel_x3'

    # This function uses the phase folders and pipeline name to set up the output directory structure,
    # e.g. 'autolens_workspace/output/phase_folder_1/phase_folder_2/pipeline_name/phase_name/'
    phase_folders = path_util.phase_folders_from_phase_folders_and_pipeline_name(phase_folders=phase_folders,
                                                                                pipeline_name=pipeline_name)

    ### PHASE 1 ###

    # In phase 1, we will fit the data with a 3 species parallel CTI model and parallel CCD filling model. In this
    # phase we will:

    # 1) Use the complete charge injection image, as opposed to extracting a sub-set of columns.
    # 2) Initialize the priors on the parallel CTI model from the results of initialize pipeline's phase 2.

    class ParallelPhase(ph.ParallelPhase):

        def pass_priors(self, results):

            self.parallel_species = results.from_phase('phase_2_parallel_x3').variable.parallel_species
            self.parallel_ccd = results.from_phase('phase_2_parallel_x3').variable.parallel_ccd
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0

    phase1 = ParallelPhase(phase_name='phase_1_parallel_x3', phase_folders=phase_folders,
                         tag_phases=tag_phases,
                         parallel_species=[prior_model.PriorModel(arctic_params.Species),
                                           prior_model.PriorModel(arctic_params.Species),
                                           prior_model.PriorModel(arctic_params.Species)],
                         parallel_ccd=arctic_params.CCD,
                         optimizer_class=nl.MultiNest, mask_function=mask_function,
                         columns=None,
                         parallel_front_edge_mask_rows=parallel_front_edge_mask_rows,
                         parallel_trails_mask_rows=parallel_trails_mask_rows,
                         parallel_total_density_range=parallel_total_density_range,
                         cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                         cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                         cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    # For the final CTI model, constant efficiency mode has a tendency to sample parameter space too fast and infer an
    # inaccurate model. Thus, we turn it off for phase 2.

    phase1.optimizer.const_efficiency_mode = False
    phase1.optimizer.n_live_points = 60
    phase1.optimizer.sampling_efficiency = 0.3

    return pl.Pipeline(pipeline_name, phase1)