# global imports
from matplotlib.path import Path, get_paths_extents
from osgeo import ogr, osr
from scipy.spatial import cKDTree
import numpy as np

# local imports
from AdcircPy.Mesh import Boundaries

# unittest imports
import unittest
import os
import matplotlib.pyplot as plt


class _ModelDomain(object):

    def __init__(self, SpatialReference, *ExternalBoundaries,
                 InternalBoundaries=None):
        self._SpatialReference = SpatialReference
        self.__set_OuterBoundary(ExternalBoundaries)
        self.__set_InnerBoundaries(InternalBoundaries)
        self.__set_DomainPath()

    def get_boundaries(self, SpatialReference=None, bbox=None, h0=None):
        OuterBoundary = self.get_outer_boundary(SpatialReference, bbox, h0)
        InnerBoundaries = self.get_inner_boundaries(SpatialReference, bbox, h0)
        return OuterBoundary, InnerBoundaries

    def get_outer_boundary(self, SpatialReference=None, bbox=None, h0=None):
        OuterBoundary = self.OuterBoundary
        if h0 is not None:
            OuterBoundary = self.__resample_Path_to_h0(OuterBoundary, h0)
        if bbox is not None:
            OuterBoundary = OuterBoundary.clip_to_bbox(bbox)
        if SpatialReference is not None:
            OuterBoundary = self.__transform_boundary(SpatialReference,
                                                      OuterBoundary)
        return OuterBoundary

    def get_inner_boundaries(self, SpatialReference=None, bbox=None, h0=None):
        InnerBoundaries = self.InnerBoundaries
        for i, boundary in enumerate(InnerBoundaries):
            if h0 is not None:
                boundary = self.__resample_Path_to_h0(boundary, h0)
            if bbox is not None:
                InnerBoundaries[i] = boundary.clip_to_bbox(bbox)
            if SpatialReference is not None:
                InnerBoundaries[i] = self.__transform_boundary(
                                                    SpatialReference, boundary)
        return InnerBoundaries

    def __set_OuterBoundary(self, ExternalBoundaries):
        """
        This function takes the external boundaries and builds a closed outer
        boundary by stitching together the open external boundaries. The outer
        boundary object is necessary for defining the concave hull of the data.
        """
        open_boundaries = list()
        for _BaseBoundary in ExternalBoundaries:
            assert isinstance(_BaseBoundary, (Boundaries.OceanBoundaries,
                                              Boundaries.LandBoundaries,
                                              Boundaries.InflowBoundaries,
                                              Boundaries.OutflowBoundaries))
            for boundary in _BaseBoundary:
                SpatialReference = boundary['SpatialReference']
                vertices = boundary['vertices']
                if not self.SpatialReference.IsSame(SpatialReference):
                    vertices = self.__transform_vertices(vertices,
                                                         SpatialReference)
                open_boundaries.append(vertices)
        if len(open_boundaries) > 0:
            ordered_vertices = open_boundaries.pop()
            while open_boundaries:
                # Take tail of ordered_vertices.
                x0, y0 = ordered_vertices[-1]
                # Find a matching head.
                heads = [boundary[0, :] for boundary in open_boundaries]
                heads_tree = cKDTree(heads)
                head_dist, hidx = heads_tree.query([x0, y0])
                # Find a matching tail
                tails = [boundary[-1, :] for boundary in open_boundaries]
                tails_tree = cKDTree(tails)
                tail_dist, tidx = tails_tree.query([x0, y0])
                if head_dist < tail_dist:
                    ordered_vertices = np.vstack([ordered_vertices,
                                                 open_boundaries.pop(hidx)])
                else:
                    ordered_vertices = np.vstack([
                                        ordered_vertices,
                                        np.flipud(open_boundaries.pop(tidx))])
            self.__OuterBoundary = Path(ordered_vertices, closed=True)
        else:
            self.__OuterBoundary = None

    def __set_InnerBoundaries(self, InternalBoundaries):
        """
        self.InnerBoundaries is a list of Path objects.
        """
        inner_boundaries = list()
        for _BaseBoundary in InternalBoundaries:
            if isinstance(_BaseBoundary, Boundaries.InnerBoundaries):
                for boundary in _BaseBoundary:
                    SpatialReference = boundary['SpatialReference']
                    vertices = boundary['vertices']
                    if not self.SpatialReference.IsSame(SpatialReference):
                        vertices = self.__transform_vertices(vertices,
                                                             SpatialReference)
                    inner_boundaries.append(vertices)
            elif isinstance(_BaseBoundary, (Boundaries.WeirBoundaries,
                                            Boundaries.CulvertBoundaries)):
                for boundary in _BaseBoundary:
                    SpatialReference = boundary['SpatialReference']
                    front_face_vertices = boundary['front_face_vertices']
                    back_face_vertices = boundary['back_face_vertices']
                    if not self.SpatialReference.IsSame(SpatialReference):
                        front_face_vertices = self.__transform_vertices(
                                                    front_face_vertices,
                                                    SpatialReference)
                        back_face_vertices = self.__transform_vertices(
                                                    back_face_vertices,
                                                    SpatialReference)
                    vertices = np.vstack([front_face_vertices,
                                          np.flipud(back_face_vertices)])
                    inner_boundaries.append(vertices)
        if len(inner_boundaries) > 0:
            self.__InnerBoundaries \
                = [Path(vertices, closed=True) for vertices
                    in inner_boundaries]
        else:
            self.__InnerBoundaries = list()

    def __set_DomainPath(self):
        if self.OuterBoundary is not None:
            self.__DomainPath = Path.make_compound_path(
                                                    *[self.OuterBoundary,
                                                      *self.InnerBoundaries])

    def __transform_vertices(self, SpatialReference, vertices):
        if not SpatialReference.IsSame(self.SpatialReference):
            CoordinateTransformation = osr.CoordinateTransformation(
                                                        self.SpatialReference,
                                                        SpatialReference)
            vertices = CoordinateTransformation.TransformPoints(vertices)
            vertices = np.asarray(vertices)
            return Path(vertices[:, :2])
        else:
            return vertices

    @staticmethod
    def __resample_Path_to_h0(Path, h0):
        if Path.codes is not None and 79 in Path.codes:
            Geom = ogr.Geometry(ogr.wkbLinearRing)
        else:
            Geom = ogr.Geometry(ogr.wkbLineString)
        for x, y in Path.vertices:
            Geom.AddPoint_2D(x, y)
        Geom.Segmentize(h0)
        return Path(Geom.GetPoints())

    @property
    def bbox(self):
        return get_paths_extents([self.DomainPath])

    @property
    def DomainPath(self):
        return self.__DomainPath

    @property
    def InnerBoundaries(self):
        return self.__InnerBoundaries

    @property
    def OuterBoundary(self):
        return self.__OuterBoundary

    @property
    def SpatialReference(self):
        return self._SpatialReference

    @property
    def _SpatialReference(self):
        return self.__SpatialReference

    # @_SpatialReference.setter
    # def _SpatialReference(self, SpatialReference):
    #     if isinstance(SpatialReference, osr.SpatialReference):
    #         self.__SpatialReference = SpatialReference
    #     elif isinstance(SpatialReference, int):
    #         self.__SpatialReference = osr.SpatialReference()
    #         self.SpatialReference.ImportFromEPSG(SpatialReference)
    #     else:
    #         raise TypeError('Unknown type for SpatialReference argument.')

    @_SpatialReference.setter
    def _SpatialReference(self, SpatialReference):
        if SpatialReference is not None:
            if isinstance(SpatialReference, int):
                EPSG = SpatialReference
                SpatialReference = osr.SpatialReference()
                SpatialReference.ImportFromEPSG(EPSG)
            else:
                assert isinstance(SpatialReference, osr.SpatialReference)
        self.__SpatialReference = SpatialReference


class ModelDomainTestCase(unittest.TestCase):

    def setUp(self):
        self.ExternalBoundaries = [
                        os.getenv('HSOFS_OCEAN_BOUNDARY_SHAPEFILE'),
                        os.getenv('HSOFS_LAND_BOUNDARIES_SHAPEFILE')]
        self.InternalBoundaries = [
                        os.getenv('HSOFS_INNER_BOUNDARIES_SHAPEFILE'),
                        os.getenv('HSOFS_WEIR_BOUNDARIES_SHAPEFILE')]
        self.epsg = 4326

    def test_external_boundaries_shapefile_instantiation(self):
        _ModelDomain(self.epsg, *self.ExternalBoundaries)

    def test_internal_boundaries_shapefile_instantiation(self):
        _ModelDomain(self.epsg, *self.ExternalBoundaries,
                     InternalBoundaries=self.InternalBoundaries)

    def test_get_outer_boundary(self):
        _ModelDomain(self.epsg, *self.ExternalBoundaries).get_outer_boundary()

    def test_get_outer_boundary_epsg(self):
        _ModelDomain(self.epsg, *self.ExternalBoundaries).get_outer_boundary(
                          SpatialReference=3395)

    def test_get_inner_boundaries(self):
        _ModelDomain(self.epsg, *self.ExternalBoundaries,
                     InternalBoundaries=self.InternalBoundaries) \
                     .get_inner_boundaries()

    def test_get_inner_boundaries_epsg(self):
        _ModelDomain(
            self.epsg,
            *self.ExternalBoundaries,
            InternalBoundaries=self.InternalBoundaries) \
           .get_inner_boundaries(SpatialReference=3395)

    def test_get_outer_boundary_from_shapefile_and_plot(self):
        OuterBoundary = _ModelDomain(self.epsg, *self.ExternalBoundaries) \
                       .get_outer_boundary()
        plt.plot(OuterBoundary.vertices[:, 0], OuterBoundary.vertices[:, 1])
        plt.title('shapefile test case')
        plt.gca().axis('scaled')
        plt.show(block=False)
