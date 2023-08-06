from autofit.tools import path_util
from autofit.optimize import non_linear as nl
from autofit.mapper import prior
from autofit.mapper import prior_model
from autocti.data import mask as msk
from autocti.pipeline import pipeline as pl
from autocti.pipeline import phase as ph
from autocti.model import arctic_params

# In this pipeline, we'll perform an analysis which fits three serial trap species to a set of charge
# injection imaging data. This will include a hyper-phase which scales the noise in the analysis, to prevent
# over-fitting the highest S/N charge injection images. The pipeline uses four phases:

# Phase 1) Fit a small section (10 rows of every charge injection) using a serial CTI model
#          with 1 trap species and a model for the serial CCD volume filling parameters.

# Phase 2) Fit a small section (again, 10 rows) using a serial CTI model with 3 trap species and a model for the serial
#          CCD volume filling parameters. The priors on trap densities and volume filling parameters are initialized
#          from the results of phase 1.

# Phase 3) Use the best-fit model from phase 2 to scale the noise of each image, to ensure that the higher and
#          lower S/N images are weighted more equally in their contribution to the likelihood.

# Phase 4) Refit the phase 2 model, using priors initialized from the results of phase 2 and the scaled noise-map
#          computed in phase 3.

def make_pipeline(phase_folders=None, tag_phases=True, mask_function=msk.Mask.empty_for_shape,
                  serial_front_edge_mask_columns=None, serial_trails_mask_columns=None,
                  serial_total_density_range=None,
                  cosmic_ray_parallel_buffer=None, cosmic_ray_serial_buffer=None, cosmic_ray_diagonal_buffer=None):

    pipeline_name = 'pipeline_hyper__serial_x3'
    
    # This function uses the phase folders and pipeline name to set up the output directory structure,
    # e.g. 'autolens_workspace/output/phase_folder_1/phase_folder_2/pipeline_name/phase_name/'
    phase_folders = path_util.phase_folders_from_phase_folders_and_pipeline_name(phase_folders=phase_folders,
                                                                                pipeline_name=pipeline_name)

    ### PHASE 1 ###

    # The best fit model of initialize pipeline's phase 2 is used to create a 'noise-scaling' map for every charge
    # injection image. These noise-scaling maps are used in conjunction with 'hyper-noise' models to scale the
    # noise-maps in a way that equally weights the fit across all charge injection images.

    class SerialHyperModelFixedPhase(ph.SerialHyperPhase):

        def pass_priors(self, results):

            self.serial_species = results.from_phase('phase_2_serial_x3').constant.serial_species
            self.serial_ccd = results.from_phase('phase_2_serial_x3').constant.serial_ccd

    phase1 = SerialHyperModelFixedPhase(phase_name='phase_1_noise_scaling', phase_folders=phase_folders,
                                        tag_phases=tag_phases,
                                        serial_species=[prior_model.PriorModel(arctic_params.Species),
                                                        prior_model.PriorModel(arctic_params.Species),
                                                        prior_model.PriorModel(arctic_params.Species)],
                                        serial_ccd=arctic_params.CCD,
                                        optimizer_class=nl.MultiNest, mask_function=mask_function,
                                        serial_front_edge_mask_columns=serial_front_edge_mask_columns,
                                        serial_trails_mask_columns=serial_trails_mask_columns,
                                        serial_total_density_range=serial_total_density_range,
                                        cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                                        cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                                        cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 30
    phase1.optimizer.sampling_efficiency = 0.2

    ### PHASE 2 ###

    # In phase 2, we will fit the data with a 3 species serial CTI model and serial CCD filling model. In this
    # phase we will:

    # 1) Use the complete charge injection image, as opposed to extracting a sub-set of rows.
    # 2) Use the scaled noise-map computed in phase 1.
    # 3) Initialize the priors on the serial CTI model from the results of initialize pipeline's phase 2.

    class SerialHyperFixedPhase(ph.SerialHyperPhase):

        def pass_priors(self, results):

            self.hyper_noise_scalars = results.from_phase('phase_1_noise_scaling').constant.hyper_noise_scalars
            self.serial_species = results.from_phase('phase_2_serial_x3').variable.serial_species
            self.serial_ccd = results.from_phase('phase_2_serial_x3').variable.serial_ccd
            self.serial_ccd.well_fill_alpha = 1.0
            self.serial_ccd.well_fill_gamma = 0.0

    phase2 = SerialHyperFixedPhase(phase_name='phase_2_serial_x3', phase_folders=phase_folders,
                                   tag_phases=tag_phases,
                                   serial_species=[prior_model.PriorModel(arctic_params.Species),
                                                   prior_model.PriorModel(arctic_params.Species),
                                                   prior_model.PriorModel(arctic_params.Species)],
                                   serial_ccd=arctic_params.CCD,
                                   optimizer_class=nl.MultiNest, mask_function=mask_function,
                                   serial_front_edge_mask_columns=serial_front_edge_mask_columns,
                                   serial_trails_mask_columns=serial_trails_mask_columns,
                                   serial_total_density_range=serial_total_density_range,
                                   cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                                   cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                                   cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    # For the final CTI model, constant efficiency mode has a tendency to sample parameter space too fast and infer an
    # inaccurate model. Thus, we turn it off for phase 2.

    phase2.optimizer.const_efficiency_mode = False
    phase2.optimizer.n_live_points = 50
    phase2.optimizer.sampling_efficiency = 0.3

    return pl.Pipeline(pipeline_name, phase1, phase2)