from autofit.tools import path_util
from autofit.optimize import non_linear as nl
from autofit.mapper import prior
from autofit.mapper import prior_model
from autocti.data import mask as msk
from autocti.pipeline import pipeline as pl
from autocti.pipeline import phase as ph
from autocti.model import arctic_params

# In this pipeline, we'll perform a basic analysis which fits a single serial trap species to a set of charge
# injection imaging data. This will include a hyper-phase which scales the noise in the analysis, to prevent
# over-fitting the highest S/N charge injection images. The pipeline uses three phases:

# Phase 1) Fit a small section (the top 10 rows of every charge injection) using a serial CTI model
#          with 1 trap species and a model for the serial CCD volume filling parameters.

# Phase 2) Use the best-fit model from phase 1 to scale the noise of each image, to ensure that the higher and
#          lower S/N images are weighted more equally in their contribution to the likelihood.

# Phase 3) Refit the phase 1 model, using priors initialized from the results of phase 1 and the scaled noise-map
#          computed in phase 2.

def make_pipeline(phase_folders=None, tag_phases=True, mask_function=msk.Mask.empty_for_shape,
                  serial_front_edge_mask_columns=None, serial_trails_mask_columns=None,
                  serial_total_density_range=None,
                  cosmic_ray_parallel_buffer=None, cosmic_ray_serial_buffer=None, cosmic_ray_diagonal_buffer=None):

    pipeline_name = 'pipeline_normal__serial_x1'

    # This function uses the phase folders and pipeline name to set up the output directory structure,
    # e.g. 'autolens_workspace/output/phase_folder_1/phase_folder_2/pipeline_name/phase_name/'
    phase_folders = path_util.phase_folders_from_phase_folders_and_pipeline_name(phase_folders=phase_folders,
                                                                                pipeline_name=pipeline_name)

    ### PHASE 1 ###

    # In phase 1, we will fit the data with a one species serial CTI model and serial CCD filling model. In this
    # phase we will:

    # 1) Use the complete charge injection image, as opposed to extracting a sub-set of rows.
    # 3) Initialize the priors on the serial CTI model from the results of phase 1 of the initialize pipeline.

    class SerialPhase(ph.SerialPhase):

        def pass_priors(self, results):

            self.serial_species = results.from_phase('phase_1_serial_x1').variable.serial_species
            self.serial_ccd = results.from_phase('phase_1_serial_x1').variable.serial_ccd
            self.serial_ccd.well_fill_alpha = 1.0
            self.serial_ccd.well_fill_gamma = 0.0

    phase1 = SerialPhase(phase_name='phase_1_serial_x1', phase_folders=phase_folders,
                           tag_phases=tag_phases,
                           serial_species=[prior_model.PriorModel(arctic_params.Species)],
                           serial_ccd=arctic_params.CCD,
                           optimizer_class=nl.MultiNest, mask_function=mask_function,
                           serial_front_edge_mask_columns=serial_front_edge_mask_columns,
                           serial_trails_mask_columns=serial_trails_mask_columns,
                         serial_total_density_range=serial_total_density_range,
                           cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                           cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                           cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    # For the final CTI model, constant efficiency mode has a tendancy to sample parameter space too fast and infer an
    # inaccurate model. Thus, we turn it off for phase 2.

    phase1.optimizer.const_efficiency_mode = False
    phase1.optimizer.n_live_points = 50
    phase1.optimizer.sampling_efficiency = 0.3

    return pl.Pipeline(pipeline_name, phase1)