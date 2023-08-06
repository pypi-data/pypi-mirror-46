# global imports
import numpy as np
from collections import defaultdict
from itertools import permutations
from matplotlib.tri import Triangulation

# unittest imports
import unittest


class NodalAttributes(dict):
    __allowed_attributes = [
        'primitive_weighting_in_continuity_equation',
        'surface_submergence_state',
        'quadratic_friction_coefficient_at_sea_floor',
        'surface_directional_effective_roughness_length',
        'surface_canopy_coefficient',
        'bridge_pilings_friction_parameters',
        'mannings_n_at_sea_floor',
        'chezy_friction_coefficient_at_sea_floor',
        'sea_surface_height_above_geoid',
        'bottom_roughness_length',
        'wave_refraction_in_swan',
        'average_horizontal_eddy_viscosity_in_sea_water_wrt_depth',
        'elemental_slope_limiter',
        'advection_state',
        'initial_river_elevation']
    __spinup_attributes = list()
    __runtime_attributes = list()

    def __init__(self, spinup_attributes=None, runtime_attributes=None,
                 **attributes):
        super(NodalAttributes, self).__init__(**attributes)
        if spinup_attributes is not None:
            for attribute in list(spinup_attributes):
                self.add_spinup_attribute(attribute)

        if runtime_attributes is not None:
            for attribute in list(runtime_attributes):
                self.add_runtime_attribute(attribute)

    def add_spinup_attribute(self, attribute):
        self.__check_allowed_attribute(attribute)
        self.__check_attribute_dictionary(attribute)
        self.spinup_attributes.append(attribute)

    def add_runtime_attribute(self, attribute):
        self.__check_allowed_attribute(attribute)
        self.__check_attribute_dictionary(attribute)
        self.runtime_attributes.append(attribute)

    def add_attribute(self, AdcircMesh, indexes, attribute_name, values,
                      default_values):
        self.__check_allowed_attribute(attribute_name)
        default_values = np.asarray(default_values)
        if values.shape[1] != default_values.shape[1]:
            raise TypeError('shapes must match.')
        raise NotImplementedError

    def __auto_generate_TAU0(self, AdcircMesh, spinup=True, runtime=True,
                             threshold_distance=1750., default_value=0.03,
                             shallow_tau0=0.02, deep_tau0=0.005,
                             threshold_depth=-10.):
        """
        Reimplementation of tau0_gen.f by Robert Weaver (2008)
        1) computes  distance to each neighboring node
        2) averages all distances to find rep. distance @ each node.
        3) Assigns a tau0 value based on depth and rep. distance.
        """
        x = AdcircMesh.get_x(SpatialReference=3395)
        y = AdcircMesh.get_x(SpatialReference=3395)
        tri = Triangulation(x, y, AdcircMesh.elements)
        neighbors = defaultdict(set)
        for simplex in tri.triangles:
            for i, j in permutations(simplex, 2):
                neighbors[i].add(j)
        points = [tuple(p) for p in np.vstack([x, y]).T]
        values = np.full(AdcircMesh.values.shape, default_value)
        for k, v in neighbors.items():
            x0, y0 = points[k]
            distances = list()
            for idx in v:
                x1, y1 = points[idx]
                distances.append(np.sqrt((x0 - x1)**2 + (y0 - y1)**2))
            distance = np.mean(distances)
            if distance >= threshold_distance:
                if AdcircMesh.values[k] >= threshold_depth:
                    values[k] = shallow_tau0
                else:
                    values[k] = deep_tau0
        indexes = np.where(values != )
        self._add_attribute('primitive_weighting_in_continuity_equation',
                           indexes, values, default_value)

        if spinup is True:
            self.add_spinup_attribute(
                                'primitive_weighting_in_continuity_equation')
        if runtime is True:
            self.add_runtime_attribute(
                                'primitive_weighting_in_continuity_equation')

    def dump(self, path, filename='fort.13'):
        if len(self.keys) > 0:
            with open(path + '/' + filename, 'r') as f:
                f.write()

    def __check_allowed_attribute(self, attribute):
        if attribute not in self.allowed_attributes:
            raise Exception('Attribute {}'.format(attribute)
                            + 'is not a recognized attribute. '
                            + 'allowed atrributes are: {}'
                            .format(self.allowed_attributes))

    def __check_attribute_dictionary(self, attribute):
        if attribute not in self.keys():
            raise RuntimeError('The attribute attribute does not exist in the '
                               'attribute table.')

    @classmethod
    def from_fort13(cls, path, spinup_attributes=None,
                    runtime_attributes=None):
        fort13 = dict()
        with open(path, 'r') as f:
            f.readline().strip()
            NP = int(f.readline().split()[0])
            NAttr = int(f.readline().split()[0])
            i = 0
            while i < NAttr:
                attribute_name = f.readline().strip()
                units = f.readline().strip()
                if units == '1':
                    units = 'unitless'
                f.readline()
                defaults = [float(x) for x in f.readline().split()]
                fort13[attribute_name] = {'units': units,
                                          'defaults': defaults}
                i += 1
            for i in range(NAttr):
                attribute_name = f.readline().strip()
                numOfNodes = int(f.readline())
                values = np.zeros((NP,
                                   len(fort13[attribute_name]['defaults'])))
                values[:] = np.nan
                j = 0
                while j < numOfNodes:
                    str = f.readline().split()
                    node_number = int(str[0])-1
                    node_values = [float(x) for x in str[1:]]
                    values[node_number, :] = node_values
                    j += 1
                values[np.where(np.isnan(values[:, 0])), :] = \
                    fort13[attribute_name]['defaults']
                fort13[attribute_name]['values'] = values
        return cls(spinup_attributes, runtime_attributes, **fort13)

    @property
    def spinup_attributes(self):
        """ """
        return self.__spinup_attributes

    @property
    def runtime_attributes(self):
        """ """
        return self.__runtime_attributes


class NodalAttributesTestCase(unittest.TestCase):
    def test_adding_1d_attribute(self):
        raise NotImplementedError
