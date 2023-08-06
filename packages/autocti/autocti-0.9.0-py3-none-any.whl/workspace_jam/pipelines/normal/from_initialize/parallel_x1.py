from autofit.tools import path_util
from autofit.optimize import non_linear as nl
from autofit.mapper import prior_model
from autocti.data import mask as msk
from autocti.pipeline import pipeline as pl
from autocti.pipeline import phase as ph
from autocti.model import arctic_params

# In this pipeline, we'll perform a basic analysis which fits a single parallel trap species to a set of charge
# injection imaging data. This will include a hyper-phase which scales the noise in the analysis, to prevent
# over-fitting the highest S/N charge injection images. The pipeline uses three phases:

# Phase 1) Fit a small section (the left-most 60 columns) of the charge injection images using a parallel CTI model
#          with 1 trap species and a model for the parallel CCD volume filling parameters.

# Phase 1h) Use the best-fit model from phase 1 to scale the noise of each image, to ensure that the higher and
#          lower S/N images are weighted more equally in their contribution to the likelihood.

# Phase 2) Refit the phase 1 model, using priors initialized from the results of phase 1 and the scaled noise-map
#          computed in phase 2.

def make_pipeline(phase_folders=None, tag_phases=True, mask_function=msk.Mask.empty_for_shape,
                  parallel_front_edge_mask_rows=None, parallel_trails_mask_rows=None,
                  parallel_total_density_range=None,
                  cosmic_ray_parallel_buffer=None, cosmic_ray_serial_buffer=None, cosmic_ray_diagonal_buffer=None):

    pipeline_name = 'pipeline_normal__parallel_x1'

    # This function uses the phase folders and pipeline name to set up the output directory structure,
    # e.g. 'autolens_workspace/output/phase_folder_1/phase_folder_2/pipeline_name/phase_name/'
    phase_folders = path_util.phase_folders_from_phase_folders_and_pipeline_name(phase_folders=phase_folders,
                                                                                pipeline_name=pipeline_name)

    ### PHASE 1 ###

    # In phase 1, we will fit the data with a one species parallel CTI model and parallel CCD filling model. In this
    # phase we will:

    # 1) Use the complete charge injection image, as opposed to extracting a sub-set of columns.
    # 2) Initialize the priors on the parallel CTI model from the results of phase 1 of the initialize pipeline.

    class ParallelPhase(ph.ParallelPhase):

        def pass_priors(self, results):

            self.parallel_species = results.from_phase('phase_1_parallel_x1').variable.parallel_species
            self.parallel_ccd = results.from_phase('phase_1_parallel_x1').variable.parallel_ccd
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0

    phase1 = ParallelPhase(phase_name='phase_1_parallel_x1', phase_folders=phase_folders,
                           tag_phases=tag_phases,
                           optimizer_class=nl.MultiNest, mask_function=mask_function,
                           columns=None,
                           parallel_front_edge_mask_rows=parallel_front_edge_mask_rows,
                           parallel_trails_mask_rows=parallel_trails_mask_rows,
                           parallel_total_density_range=parallel_total_density_range,
                           cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                           cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                           cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    phase1.optimizer.const_efficiency_mode = False
    phase1.optimizer.n_live_points = 50
    phase1.optimizer.sampling_efficiency = 0.3

    return pl.Pipeline(pipeline_name, phase1)