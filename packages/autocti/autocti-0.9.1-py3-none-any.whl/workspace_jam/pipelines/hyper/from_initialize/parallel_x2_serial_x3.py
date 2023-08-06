from autofit.tools import path_util
from autofit.optimize import non_linear as nl
from autofit.mapper import prior
from autofit.mapper import prior_model
from autocti.data import mask as msk
from autocti.pipeline import pipeline as pl
from autocti.pipeline import phase as ph
from autocti.model import arctic_params

# In this pipeline, we'll perform an analysis which fits two parallel trap species to a set of charge
# injection imaging data. This will include a hyper-phase which scales the noise in the analysis, to prevent
# over-fitting the highest S/N charge injection images. The pipeline uses four phases:

# Phase 1) Fit a small section (60 columns of every charge injection) using a parallel CTI model
#          with 1 trap species and a model for the parallel CCD volume filling parameters.

# Phase 2) Fit a small section (again, 60 columns) using a parallel CTI model with 2 trap species and a model for the
#          parallel CCD volume filling parameters. The priors on trap densities and volume filling parameters are
#          initialized from the results of phase 1.

# Phase 3) Use the best-fit model from phase 2 to scale the noise of each image, to ensure that the higher and
#          lower S/N images are weighted more equally in their contribution to the likelihood.

# Phase 4) Refit the phase 2 model, using priors initialized from the results of phase 2 and the scaled noise-map
#          computed in phase 3.

def make_pipeline(phase_folders=None, tag_phases=True, mask_function=msk.Mask.empty_for_shape,
                  parallel_front_edge_mask_rows=None, parallel_trails_mask_rows=None,
                  serial_front_edge_mask_columns=None, serial_trails_mask_columns=None,
                  parallel_total_density_range=None, serial_total_density_range=None,
                  cosmic_ray_parallel_buffer=None, cosmic_ray_serial_buffer=None, cosmic_ray_diagonal_buffer=None):

    pipeline_name = 'pipeline__hyper_parallel_x2_serial'

    # This function uses the phase folders and pipeline name to set up the output directory structure,
    # e.g. 'autolens_workspace/output/phase_folder_1/phase_folder_2/pipeline_name/phase_name/'
    phase_folders = path_util.phase_folders_from_phase_folders_and_pipeline_name(phase_folders=phase_folders,
                                                                                pipeline_name=pipeline_name)

    ### PHASE 1 ###

    # In phase 1, we will fit the data with a two species parallel and three species serial CTI model. In this
    # phase we will:

    # 1) Initialize the priors on this model from phases 2 and 4 of the pipeline.

    class ParallelSerialPhase(ph.ParallelSerialPhase):

        def pass_priors(self, results):
            
            self.parallel_ccd = results.from_phase('phase_2_parallel_x2').variable.parallel_ccd
            self.parallel_species = results.from_phase('phase_2_parallel_x2').variable.parallel_species
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0
            self.serial_ccd = results.from_phase('phase_4_serial_x3').variable.serial_ccd
            self.serial_species = results.from_phase('phase_4_serial_x3').variable.serial_species
            self.serial_ccd.well_fill_alpha = 1.0
            self.serial_ccd.well_fill_gamma = 0.0

    phase1 = ParallelSerialPhase(phase_name='phase_1_parallel_x2_serial_x3', 
                                 phase_folders=phase_folders,
                                 tag_phases=tag_phases,
                                 parallel_species=[prior_model.PriorModel(arctic_params.Species),
                                                   prior_model.PriorModel(arctic_params.Species)],
                                 parallel_ccd=arctic_params.CCD,
                                 serial_species=[prior_model.PriorModel(arctic_params.Species),
                                                 prior_model.PriorModel(arctic_params.Species),
                                                 prior_model.PriorModel(arctic_params.Species)],
                                 serial_ccd=arctic_params.CCD,
                                 optimizer_class=nl.MultiNest, mask_function=mask_function,
                                 parallel_front_edge_mask_rows=parallel_front_edge_mask_rows,
                                 parallel_trails_mask_rows=parallel_trails_mask_rows,
                                 serial_front_edge_mask_columns=serial_front_edge_mask_columns,
                                 serial_trails_mask_columns=serial_trails_mask_columns,
                                 parallel_total_density_range=parallel_total_density_range,
                                 serial_total_density_range=serial_total_density_range,
                                 cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                                 cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                                 cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 80
    phase1.optimizer.sampling_efficiency = 0.2

    ### PHASE 2 ###

    # The best fit model of phase 2 is used to create a 'noise-scaling' map for every charge injection image. These
    # noise-scaling maps are used in conjunction with 'hyper-noise' models to scale the noise-maps in a way that
    # equally weights the fit across all charge injection images.

    class ParallelSerialHyperModelFixedPhase(ph.ParallelSerialHyperPhase):

        def pass_priors(self, results):

            self.parallel_species = \
                results.from_phase('phase_1_parallel_x2_serial_x3').constant.parallel_species
            self.parallel_ccd = \
                results.from_phase('phase_1_parallel_x2_serial_x3').constant.parallel_ccd
            self.serial_species = \
                results.from_phase('phase_1_parallel_x2_serial_x3').constant.serial_species
            self.serial_ccd = \
                results.from_phase('phase_1_parallel_x2_serial_x3').constant.serial_ccd

    phase2 = ParallelSerialHyperModelFixedPhase(phase_name='phase_2_noise_scaling', phase_folders=phase_folders,
                                                tag_phases=tag_phases,
                                                parallel_species=[prior_model.PriorModel(arctic_params.Species),
                                                                  prior_model.PriorModel(arctic_params.Species)],
                                                parallel_ccd=arctic_params.CCD,
                                                serial_species=[prior_model.PriorModel(arctic_params.Species),
                                                                prior_model.PriorModel(arctic_params.Species),
                                                                prior_model.PriorModel(arctic_params.Species)],
                                                serial_ccd=arctic_params.CCD,
                                                optimizer_class=nl.MultiNest, mask_function=mask_function,
                                                parallel_front_edge_mask_rows=parallel_front_edge_mask_rows,
                                                parallel_trails_mask_rows=parallel_trails_mask_rows,
                                                serial_front_edge_mask_columns=serial_front_edge_mask_columns,
                                                serial_trails_mask_columns=serial_trails_mask_columns,
                                                parallel_total_density_range=parallel_total_density_range,
                                                serial_total_density_range=serial_total_density_range,
                                                cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                                                cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                                                cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    phase2.optimizer.const_efficiency_mode = True
    phase2.optimizer.nr_live_points = 30
    phase2.optimizer.sampling_efficiency = 0.2

    ### PHASE 3 ###

    # In phase 3, we will fit the data with a 2 species parallel and 3 species serial CTI model. In this
    # phase we will:

    # 1) Use the scaled noise-map computed in phase 2.
    # 2) Initialize the priors on the parallel and serial CTI models from the results of phase 1.

    class ParallelSerialHyperFixedPhase(ph.ParallelSerialHyperPhase):

        def pass_priors(self, results):

            self.hyper_noise_scalars = results.from_phase('phase_2_noise_scaling').constant.hyper_noise_scalars

            self.parallel_species = \
                results.from_phase('phase_1_parallel_x2_serial_x3').variable.parallel_species
            self.parallel_ccd = \
                results.from_phase('phase_1_parallel_x2_serial_x3').variable.parallel_ccd
            self.parallel_ccd.well_fill_alpha = 1.0
            self.parallel_ccd.well_fill_gamma = 0.0

            self.serial_species = \
                results.from_phase('phase_1_parallel_x2_serial_x3').variable.serial_species
            self.serial_ccd = \
                results.from_phase('phase_1_parallel_x2_serial_x3').variable.serial_ccd
            self.serial_ccd.well_fill_alpha = 1.0
            self.serial_ccd.well_fill_gamma = 0.0

    phase3 = ParallelSerialHyperFixedPhase(phase_name='phase_3_parallel_x2_serial_x3_species', phase_folders=phase_folders,
                                           tag_phases=tag_phases,
                                           parallel_species=[prior_model.PriorModel(arctic_params.Species),
                                                             prior_model.PriorModel(arctic_params.Species)],
                                           parallel_ccd=arctic_params.CCD,
                                           serial_species=[prior_model.PriorModel(arctic_params.Species),
                                                           prior_model.PriorModel(arctic_params.Species),
                                                           prior_model.PriorModel(arctic_params.Species)],
                                           serial_ccd=arctic_params.CCD,
                                           optimizer_class=nl.MultiNest, mask_function=mask_function,
                                           parallel_front_edge_mask_rows=parallel_front_edge_mask_rows,
                                           parallel_trails_mask_rows=parallel_trails_mask_rows,
                                           serial_front_edge_mask_columns=serial_front_edge_mask_columns,
                                           serial_trails_mask_columns=serial_trails_mask_columns,
                                           parallel_total_density_range=parallel_total_density_range,
                                           serial_total_density_range=serial_total_density_range,
                                           cosmic_ray_parallel_buffer=cosmic_ray_parallel_buffer,
                                           cosmic_ray_serial_buffer=cosmic_ray_serial_buffer,
                                           cosmic_ray_diagonal_buffer=cosmic_ray_diagonal_buffer)

    # For the final CTI model, constant efficiency mode has a tendency to sample parameter space too fast and infer an
    # inaccurate model. Thus, we turn it off for phase 2.

    phase3.optimizer.const_efficiency_mode = False
    phase3.optimizer.n_live_points = 50
    phase3.optimizer.sampling_efficiency = 0.3

    return pl.Pipeline(pipeline_name, phase1, phase2, phase3)