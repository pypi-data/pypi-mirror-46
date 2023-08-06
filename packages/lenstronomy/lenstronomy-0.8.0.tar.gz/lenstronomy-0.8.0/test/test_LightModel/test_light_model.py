__author__ = 'sibirrer'

import numpy as np
import numpy.testing as npt
import pytest
import lenstronomy.Util.param_util as param_util
from lenstronomy.LightModel.light_model import LightModel


class TestLightModel(object):
    """
    tests the source model routines
    """

    def setup(self):
        self.light_model_list = ['GAUSSIAN', 'MULTI_GAUSSIAN', 'SERSIC', 'SERSIC_ELLIPSE',
                                 'CORE_SERSIC', 'SHAPELETS', 'HERNQUIST',
                                 'HERNQUIST_ELLIPSE', 'PJAFFE', 'PJAFFE_ELLIPSE', 'UNIFORM', 'POWER_LAW', 'NIE',
                                 'INTERPOL'
                                 ]
        phi_G, q = 0.5, 0.8
        e1, e2 = param_util.phi_q2_ellipticity(phi_G, q)
        self.kwargs = [
            {'amp': 1., 'sigma_x': 1, 'sigma_y': 1., 'center_x': 0, 'center_y': 0},  # 'GAUSSIAN'
            {'amp': [1., 2], 'sigma': [1, 3], 'center_x': 0, 'center_y': 0},  # 'MULTI_GAUSSIAN'
            {'amp': 1, 'R_sersic': 0.5, 'n_sersic': 1, 'center_x': 0, 'center_y': 0},  # 'SERSIC'
            {'amp': 1, 'R_sersic': 0.5, 'n_sersic': 1, 'e1': e1, 'e2': e2, 'center_x': 0, 'center_y': 0},  # 'SERSIC_ELLIPSE'
            {'amp': 1, 'R_sersic': 0.5, 'Re': 0.1, 'gamma': 2., 'n_sersic': 1, 'e1': e1, 'e2': e2, 'center_x': 0, 'center_y': 0},
            # 'CORE_SERSIC'
            {'amp': [1, 1, 1], 'beta': 0.5, 'n_max': 1, 'center_x': 0, 'center_y': 0},  # 'SHAPELETS'
            {'amp': 1, 'Rs': 0.5, 'center_x': 0, 'center_y': 0},  # 'HERNQUIST'
            {'amp': 1, 'Rs': 0.5, 'center_x': 0, 'center_y': 0, 'e1': e1, 'e2': e2},  # 'HERNQUIST_ELLIPSE'
            {'amp': 1, 'Ra': 1, 'Rs': 0.5, 'center_x': 0, 'center_y': 0},  # 'PJAFFE'
            {'amp': 1, 'Ra': 1, 'Rs': 0.5, 'center_x': 0, 'center_y': 0, 'e1': e1, 'e2': e2},  # 'PJAFFE_ELLIPSE'
            {'amp': 1},  # 'UNIFORM'
            {'amp': 1., 'gamma': 2., 'e1': e1, 'e2': e2, 'center_x': 0, 'center_y': 0},  # 'POWER_LAW'
            {'amp': .001, 'e1': 0, 'e2': 1., 'center_x': 0, 'center_y': 0, 's_scale': 1.},  # 'NIE'
            {'image': np.zeros((10, 10)), 'scale': 1, 'phi_G': 0, 'center_x': 0, 'center_y': 0}
            ]

        self.LightModel = LightModel(light_model_list=self.light_model_list)

    def test_init(self):
        model_list = ['CORE_SERSIC', 'SHAPELETS', 'SHAPELETS_POLAR', 'SHAPELETS_POLAR_EXP', 'UNIFORM', 'CHAMELEON', 'DOUBLE_CHAMELEON']
        lightModel = LightModel(light_model_list=model_list)
        assert len(lightModel.profile_type_list) == len(model_list)

    def test_surface_brightness(self):
        output = self.LightModel.surface_brightness(x=1, y=1, kwargs_list=self.kwargs)
        npt.assert_almost_equal(output, 3.512593731652167, decimal=6)

    def test_surface_brightness_array(self):
        output = self.LightModel.surface_brightness(x=[1], y=[1], kwargs_list=self.kwargs)
        npt.assert_almost_equal(output[0], 3.512593731652167, decimal=6)

    def test_functions_split(self):
        output = self.LightModel.functions_split(x=1., y=1., kwargs_list=self.kwargs)
        npt.assert_almost_equal(output[0][0],0.058549831524319168, decimal=6)

    def test_re_normalize_flux(self):
        kwargs_out = self.LightModel.re_normalize_flux(kwargs_list=self.kwargs, norm_factor=2)
        assert kwargs_out[0]['amp'] == 2 * self.kwargs[0]['amp']

    def test_param_name_list(self):
        param_name_list = self.LightModel.param_name_list()
        assert len(self.light_model_list) == len(param_name_list)

    def test_update_linear(self):
        response, n = self.LightModel.functions_split(1, 1, self.kwargs)
        param = np.ones(n) * 2
        kwargs_out, i = self.LightModel.update_linear(param, i=0, kwargs_list=self.kwargs)
        assert i == n
        assert kwargs_out[0]['amp'] == 2

    def test_total_flux(self):
        light_model_list = ['SERSIC', 'SERSIC_ELLIPSE', 'INTERPOL', 'GAUSSIAN', 'GAUSSIAN_ELLIPSE', 'MULTI_GAUSSIAN',
                            'MULTI_GAUSSIAN_ELLIPSE']
        kwargs_list = [{'amp': 1, 'R_sersic': 0.5, 'n_sersic': 1, 'center_x': 0, 'center_y': 0},  # 'SERSIC'
                       {'amp': 1, 'R_sersic': 0.5, 'n_sersic': 1, 'e1': 0.1, 'e2': 0, 'center_x': 0, 'center_y': 0},  # 'SERSIC_ELLIPSE'
                       {'image': np.ones((10, 10)), 'scale': 1, 'phi_G': 0, 'center_x': 0, 'center_y': 0},  # 'INTERPOL'
                       {'amp': 2, 'sigma_x': 2, 'sigma_y': 1, 'center_x': 0, 'center_y': 0},  # 'GAUSSIAN'
                       {'amp': 2, 'sigma': 2, 'e1': 0.1, 'e2': 0, 'center_x': 0, 'center_y': 0},  # 'GAUSSIAN_ELLIPSE'
                       {'amp': [1,1], 'sigma': [2, 1], 'center_x': 0, 'center_y': 0},  # 'MULTI_GAUSSIAN'
                       {'amp': [1, 1], 'sigma': [2, 1], 'e1': 0.1, 'e2': 0, 'center_x': 0, 'center_y': 0}  # 'MULTI_GAUSSIAN_ELLIPSE'
                      ]
        lightModel = LightModel(light_model_list=light_model_list)
        total_flux_list = lightModel.total_flux(kwargs_list)
        assert total_flux_list[2] == 100
        assert total_flux_list[3] == 2
        assert total_flux_list[4] == 2
        assert total_flux_list[5] == 2
        assert total_flux_list[6] == 2

        total_flux_list = lightModel.total_flux(kwargs_list, norm=True)
        assert total_flux_list[2] == 100
        assert total_flux_list[3] == 1
        assert total_flux_list[4] == 1
        assert total_flux_list[5] == 2
        assert total_flux_list[6] == 2


if __name__ == '__main__':
    pytest.main()
