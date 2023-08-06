__author__ = 'sibirrer'

import pytest
import lenstronomy.Util.simulation_util as sim_util
from lenstronomy.ImSim.image_model import ImageModel
import lenstronomy.Util.param_util as param_util
from lenstronomy.PointSource.point_source import PointSource
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.LightModel.light_model import LightModel
from lenstronomy.Plots.output_plots import LensModelPlot
import lenstronomy.Plots.output_plots as output_plots
from lenstronomy.Data.imaging_data import ImageData
from lenstronomy.Data.psf import PSF

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np


class TestOutputPlots(object):
    """
    test the fitting sequences
    """
    def setup(self):

        # data specifics
        sigma_bkg = 0.05  # background noise per pixel
        exp_time = 100  # exposure time (arbitrary units, flux per pixel is in units #photons/exp_time unit)
        numPix = 10  # cutout pixel size
        deltaPix = 0.5  # pixel size in arcsec (area per pixel = deltaPix**2)
        fwhm = 0.5  # full width half max of PSF

        # PSF specification

        self.kwargs_data = sim_util.data_configure_simple(numPix, deltaPix, exp_time, sigma_bkg)
        data_class = ImageData(**self.kwargs_data)
        kwargs_psf_gaussian = {'psf_type': 'GAUSSIAN', 'fwhm': fwhm, 'truncation': 5, 'pixel_size': deltaPix}
        psf_gaussian = PSF(**kwargs_psf_gaussian)
        self.kwargs_psf = {'psf_type': 'PIXEL', 'kernel_point_source': psf_gaussian.kernel_point_source}
        psf_class = PSF(**self.kwargs_psf)

        # 'EXERNAL_SHEAR': external shear
        kwargs_shear = {'e1': 0.01, 'e2': 0.01}  # gamma_ext: shear strength, psi_ext: shear angel (in radian)
        e1, e2 = param_util.phi_q2_ellipticity(0.2, 0.8)
        kwargs_spemd = {'theta_E': 1., 'gamma': 1.8, 'center_x': 0, 'center_y': 0, 'e1': e1, 'e2': e2}

        lens_model_list = ['SPEP', 'SHEAR']
        self.kwargs_lens = [kwargs_spemd, kwargs_shear]
        lens_model_class = LensModel(lens_model_list=lens_model_list)
        self.LensModel = lens_model_class
        # list of light profiles (for lens and source)
        # 'SERSIC': spherical Sersic profile
        kwargs_sersic = {'amp': 1., 'R_sersic': 0.1, 'n_sersic': 2, 'center_x': 0, 'center_y': 0}
        # 'SERSIC_ELLIPSE': elliptical Sersic profile
        phi, q = 0.2, 0.9
        e1, e2 = param_util.phi_q2_ellipticity(phi, q)
        kwargs_sersic_ellipse = {'amp': 1., 'R_sersic': .6, 'n_sersic': 7, 'center_x': 0, 'center_y': 0,
                                 'e1': e1, 'e2': e2}

        lens_light_model_list = ['SERSIC']
        self.kwargs_lens_light = [kwargs_sersic]
        lens_light_model_class = LightModel(light_model_list=lens_light_model_list)
        source_model_list = ['SERSIC_ELLIPSE']
        self.kwargs_source = [kwargs_sersic_ellipse]
        source_model_class = LightModel(light_model_list=source_model_list)
        self.kwargs_ps = [{'ra_source': 0.0, 'dec_source': 0.0,
                           'source_amp': 1.}]  # quasar point source position in the source plane and intrinsic brightness
        point_source_list = ['SOURCE_POSITION']
        point_source_class = PointSource(point_source_type_list=point_source_list, fixed_magnification_list=[True])
        kwargs_numerics = {'supersampling_factor': 1}
        imageModel = ImageModel(data_class, psf_class, lens_model_class, source_model_class,
                                lens_light_model_class,
                                point_source_class, kwargs_numerics=kwargs_numerics)
        image_sim = sim_util.simulate_simple(imageModel, self.kwargs_lens, self.kwargs_source,
                                         self.kwargs_lens_light, self.kwargs_ps)

        data_class.update_data(image_sim)
        self.kwargs_data['image_data'] = image_sim
        self.kwargs_model = {'lens_model_list': lens_model_list,
                               'source_light_model_list': source_model_list,
                               'lens_light_model_list': lens_light_model_list,
                               'point_source_model_list': point_source_list,
                               'fixed_magnification_list': [False],
                             }
        self.kwargs_numerics = kwargs_numerics
        self.data_class = ImageData(**self.kwargs_data)

    def test_lensModelPlot(self):

        lensPlot = LensModelPlot(self.kwargs_data, self.kwargs_psf, self.kwargs_numerics, self.kwargs_model,
                                     self.kwargs_lens, self.kwargs_source, self.kwargs_lens_light, self.kwargs_ps,
                                     arrow_size=0.02, cmap_string="gist_heat")

        lensPlot.plot_main(image_names=True, with_caustics=True)
        plt.close()

        #f, axes = plt.subplots(2, 3, figsize=(16, 8))

        #lensPlot.data_plot(ax=axes[0, 0])
        #lensPlot.model_plot(ax=axes[0, 1])
        #lensPlot.normalized_residual_plot(ax=axes[0, 2], v_min=-6, v_max=6)
        #lensPlot.source_plot(ax=axes[1, 0], convolution=False, deltaPix_source=0.01, numPix=100)
        #lensPlot.convergence_plot(ax=axes[1, 1], v_max=1)
        #lensPlot.magnification_plot(ax=axes[1, 2])
        #plt.close()

        lensPlot.plot_separate()
        plt.close()
        #f, axes = plt.subplots(2, 3, figsize=(16, 8))

        #lensPlot.decomposition_plot(ax=axes[0, 0], text='Lens light', lens_light_add=True, unconvolved=True)
        #lensPlot.decomposition_plot(ax=axes[1, 0], text='Lens light convolved', lens_light_add=True)
        #lensPlot.decomposition_plot(ax=axes[0, 1], text='Source light', source_add=True, unconvolved=True)
        #lensPlot.decomposition_plot(ax=axes[1, 1], text='Source light convolved', source_add=True)
        #lensPlot.decomposition_plot(ax=axes[0, 2], text='All components', source_add=True, lens_light_add=True,
        #                                unconvolved=True)
        #lensPlot.decomposition_plot(ax=axes[1, 2], text='All components convolved', source_add=True,
        #                                lens_light_add=True, point_source_add=True)
        #plt.close()
        lensPlot.plot_subtract_from_data_all()
        plt.close()
        #f, axes = plt.subplots(2, 3, figsize=(16, 8))

        #lensPlot.subtract_from_data_plot(ax=axes[0,0], text='Data')
        #lensPlot.subtract_from_data_plot(ax=axes[0,1], text='Data - Point Source', point_source_add=True)
        #lensPlot.subtract_from_data_plot(ax=axes[0,2], text='Data - Lens Light', lens_light_add=True)
        #lensPlot.subtract_from_data_plot(ax=axes[1,0], text='Data - Source Light', source_add=True)
        #lensPlot.subtract_from_data_plot(ax=axes[1,1], text='Data - Source Light - Point Source', source_add=True, point_source_add=True)
        #lensPlot.subtract_from_data_plot(ax=axes[1,2], text='Data - Lens Light - Point Source', lens_light_add=True, point_source_add=True)
        #plt.close()

        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        lensPlot.deflection_plot(ax=ax, with_caustics=True, axis=1)
        plt.close()

        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        lensPlot.deflection_plot(ax=ax, with_caustics=True, axis=0)
        plt.close()

        numPix = 100
        deltaPix_source = 0.01
        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        lensPlot.error_map_source_plot(ax, numPix, deltaPix_source, with_caustics=True)
        plt.close()

        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        lensPlot.absolute_residual_plot(ax=ax)
        plt.close()

    def test_psf_iteration_compare(self):
        kwargs_psf = self.kwargs_psf
        kwargs_psf['kernel_point_source_init'] = kwargs_psf['kernel_point_source']
        f, ax = output_plots.psf_iteration_compare(kwargs_psf=kwargs_psf, vmin=-1, vmax=1)
        plt.close()
        f, ax = output_plots.psf_iteration_compare(kwargs_psf=kwargs_psf)
        plt.close()

    def test_external_shear_direction(self):
        f, ax = output_plots.ext_shear_direction(data_class=self.data_class, lens_model_class=self.LensModel, kwargs_lens=self.kwargs_lens,
                        strength_multiply=10)
        plt.close()

    def test_plot_chain(self):
        X2_list = [1, 1, 2]
        pos_list = [[1, 0], [2, 0], [3, 0]]
        vel_list = [[-1, 0], [0, 0], [1, 0]]
        param_list = ['test1', 'test2']
        chain = X2_list, pos_list, vel_list, None
        output_plots.plot_chain(chain=chain, param_list=param_list)
        plt.close()

    def test_plot_mcmc_behaviour(self):
        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        param_mcmc = ['a', 'b']
        samples_mcmc = np.random.random((10, 1000))
        dist_mcmc = np.random.random(1000)
        output_plots.plot_mcmc_behaviour(ax, samples_mcmc, param_mcmc, dist_mcmc, num_average=10)
        plt.close()

    def test_scale_bar(self):
        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        output_plots.scale_bar(ax, 3, dist=1, text='1"', flipped=True)
        plt.close()
        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        output_plots.text_description(ax, d=3, text='test', color='w', backgroundcolor='k', flipped=True)
        plt.close()

    def test_lens_model_plot(self):
        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        lensModel = LensModel(lens_model_list=['SIS'])
        kwargs_lens = [{'theta_E': 1., 'center_x': 0, 'center_y': 0}]
        output_plots.lens_model_plot(ax, lensModel, kwargs_lens, numPix=10, deltaPix=0.5, sourcePos_x=0, sourcePos_y=0,
                    point_source=True, with_caustics=True)
        plt.close()

    def test_arrival_time_surface(self):
        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        lensModel = LensModel(lens_model_list=['SIS'])
        kwargs_lens = [{'theta_E': 1., 'center_x': 0, 'center_y': 0}]
        output_plots.arrival_time_surface(ax, lensModel, kwargs_lens, numPix=10, deltaPix=0.5, sourcePos_x=0, sourcePos_y=0,
                                     point_source=True, with_caustics=True)
        plt.close()
        f, ax = plt.subplots(1, 1, figsize=(4, 4))
        lensModel = LensModel(lens_model_list=['SIS'])
        kwargs_lens = [{'theta_E': 1., 'center_x': 0, 'center_y': 0}]
        output_plots.arrival_time_surface(ax, lensModel, kwargs_lens, numPix=10, deltaPix=0.5, sourcePos_x=0,
                                          sourcePos_y=0,
                                          point_source=False, with_caustics=False)
        plt.close()


if __name__ == '__main__':
    pytest.main()
