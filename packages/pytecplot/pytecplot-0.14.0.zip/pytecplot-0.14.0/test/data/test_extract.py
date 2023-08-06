# coding: utf-8
from __future__ import unicode_literals

import base64, itertools as it, os, platform, sys, unittest, zlib

import numpy as np
from numpy import random as rand

from ctypes import *
from tempfile import NamedTemporaryFile
from unittest.mock import patch, Mock, PropertyMock

import tecplot as tp
from tecplot import session
from tecplot.constant import *
from tecplot.exception import *

from test import patch_tecutil, skip_if_sdk_version_before, mocked_sdk_version

from ..sample_data import sample_data_file

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.filenames = [
            sample_data_file('10x10x10'),
            sample_data_file('3x3_2x2')]

    def tearDown(self):
        tp.new_layout()
        for f in self.filenames:
            os.remove(f)

    @skip_if_sdk_version_before(2017, 3)
    def test_extract_default_args(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        z = tp.data.extract.extract_slice(origin=(.5,.5,0), normal=(0,1,0),
            source=SliceSource.VolumeZones, mode=ExtractMode.SingleZone,
            copy_cell_centers=False, assign_strand_ids=False, frame=None,
            dataset=None)

        self.assertIsInstance(z, tp.data.ClassicFEZone)

        with mocked_sdk_version(2017, 2):
            with self.assertRaises(TecplotInterfaceChangeError):
                z = tp.data.extract.extract_slice(origin=(.5,.5,0),
                    normal=(0,1,0), mode=ExtractMode.SingleZone)

    @skip_if_sdk_version_before(2017, 3)
    def test_extract_nondefault_args(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        z = tp.data.extract.extract_slice(origin=(.5,.5,0), normal=(0,1,0),
            source=SliceSource.VolumeZones,
            mode=ExtractMode.OneZonePerConnectedRegion, copy_cell_centers=True,
            assign_strand_ids=True, frame=fr, dataset=None)

        self.assertIsInstance(z, list)
        self.assertEqual(len(z), 1)

        with self.assertRaises(TecplotInterfaceChangeError):
            z = tp.data.extract.extract_slice((0,0,0), (0,0,1),
                                              multiple_zones=True)

    def test_dataset_frame_mismatch(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        newfr = tp.active_page().add_frame()
        newfr.create_dataset('D', ['x','y'])

        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            z = tp.data.extract.extract_slice(dataset=ds, frame=newfr)

    @skip_if_sdk_version_before(2017, 3)
    def test_interpolate_linear(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])

        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        z = tp.data.extract.extract_slice(origin=(0.5,0.5,0), normal=(0,1,0),
            source=SliceSource.VolumeZones, dataset=ds)
        self.assertIn(z, ds)
        self.assertEqual(z.name, 'Slice: Y=0.5')

    def test_interpolate_linear_failures(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])

        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        with patch_tecutil('CreateSliceZoneFromPlneX', return_value=False):
            with self.assertRaises(TecplotSystemError):
                tp.data.extract.extract_slice((0.5,0.5,0), (0,1,0))

        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            tp.data.extract.extract_slice((0.5,0.5,100), (0,0,1))

        if __debug__:
            tp.new_layout()
            ds = tp.data.load_tecplot(self.filenames[1])

            fr = tp.active_frame()
            fr.plot_type = PlotType.Cartesian2D
            with self.assertRaises(TecplotLogicError):
                tp.data.extract.extract_slice((0.5,0.5,0), (0,1,0))

        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[1])

        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D
        with self.assertRaises(TecplotLogicError):
            tp.data.extract.extract_slice((0.5,0.5,0), (0,1,0))

    def test_extract_line_3d(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian3D

        pts = [
            (.5, .5, .5),
            (.8, .8, .8),
            (1., 1., 1.)]
        z = tp.data.extract.extract_line(pts)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (3,))

        pts = [
            (.5, .5, .5),
            (.8, .8, .8),
            (1., 1., 1.)]
        z = tp.data.extract.extract_line(pts, num_points=10)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (10,))

        def pts():
            for p in ((.5, .5, .5), (.8, .8, .8), (1., 1., 1.)):
                yield p
        z = tp.data.extract.extract_line(pts())
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (3,))

        pts = [
            (.5, .5, .5),
            (.8, .8, .8),
            (1.1, 1.1, 1.1)]
        z = tp.data.extract.extract_line(pts)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (2,))

        pts = [(1.1, 1.1, 1.1)]
        nzones = ds.num_zones
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            z = tp.data.extract.extract_line(pts)
        self.assertEqual(nzones, ds.num_zones)

    def test_extract_line_2d(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filenames[0])
        fr = tp.active_frame()
        fr.plot_type = PlotType.Cartesian2D
        fr.plot().fieldmap(0).surfaces.surfaces_to_plot = SurfacesToPlot.KPlanes

        pts = [
            (.5, .5),
            (.8, .8),
            (1., 1.)]
        z = tp.data.extract.extract_line(pts, frame=fr)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (3,))

        pts = [
            (.5, .5),
            (.8, .8),
            (1.1, 1.1)]
        z = tp.data.extract.extract_line(pts, dataset=ds)
        self.assertIsInstance(z, tp.data.OrderedZone)
        self.assertEqual(z.values(0).shape, (2,))

        pts = [(1.1, 1.1)]
        nzones = ds.num_zones
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            z = tp.data.extract.extract_line(pts, frame=fr, dataset=ds)
        self.assertEqual(nzones, ds.num_zones)

    def test_extract_line_failures(self):
        if __debug__:
            tp.new_layout()
            ds = tp.data.load_tecplot(self.filenames[0])
            fr = tp.active_frame()

            pts = [
                (.5, .5, .5),
                (.8, .8, .8),
                (1., 1., 1.)]

            fr.plot_type = PlotType.Sketch

            with self.assertRaises(TecplotLogicError):
                z = tp.data.extract.extract_line(pts)

            fr.plot_type = PlotType.Cartesian3D
            fr2 = tp.active_page().add_frame()
            ds2 = tp.data.load_tecplot(self.filenames[0])
            with self.assertRaises(TecplotLogicError):
                z = tp.data.extract.extract_line(pts, frame=fr, dataset=ds2)

    @skip_if_sdk_version_before(2017, 3)
    def test_extract_modes(self):
        rand.seed(1)
        tp.new_layout()
        fr = tp.active_frame()
        ds = fr.create_dataset('D', ['x', 'y', 'z', 's'])

        # Create a single FE Brick zone with two disconnected regions
        x = np.linspace(-1, 1, 3)
        y = np.linspace(-1, 1, 4)
        z = np.linspace(-1, 1, 5)
        nodes = list(it.product(x, y, z))
        shape = (len(x), len(y), len(z))
        cells = []
        for i, j, k in it.product(*[range(s - 1) for s in shape]):
            cell = []
            for ii, jj in it.product([i, i+1], [j, j+1]):
                for kk in [k, k+1] if jj == j else [k+1, k]:
                    cell.append(ii * len(y) * len(z) + jj * len(z) + kk)
            cells.append(cell)

        z = np.linspace(2, 4, 5)
        node_offset = len(nodes)
        nodes.extend(list(it.product(x, y, z)))
        shape = (len(x), len(y), len(z))
        for i, j, k in it.product(*[range(s - 1) for s in shape]):
            cell = []
            for ii, jj in it.product([i, i+1], [j, j+1]):
                for kk in [k, k+1] if jj == j else [k+1, k]:
                    cell.append(ii * len(y) * len(z) + jj * len(z) + kk + node_offset)
            cells.append(cell)

        zn = ds.add_fe_zone(ZoneType.FEBrick, 'Z', num_points=len(nodes),
                            num_elements=len(cells))

        zn.values('x')[:] = [n[0] for n in nodes]
        zn.values('y')[:] = [n[1] for n in nodes]
        zn.values('z')[:] = [n[2] for n in nodes]
        zn.values('s')[:] = rand.uniform(-10, 10, len(nodes))

        zn.nodemap[:] = cells

        fr.plot_type = PlotType.Cartesian3D

        self.assertEqual(ds.num_zones, 1)
        zn = tp.data.extract.extract_slice((0.25,0.25,0), (1,1,0),
            mode=ExtractMode.SingleZone)
        self.assertIsInstance(zn, tp.data.zone.Zone)
        self.assertEqual(ds.num_zones, 2)
        zns = tp.data.extract.extract_slice((0.25,0.25,0), (1,1,0),
            mode=ExtractMode.OneZonePerSourceZone)
        self.assertEqual(len(zns), 1)
        self.assertIsInstance(zns[0], tp.data.zone.Zone)
        self.assertEqual(ds.num_zones, 3)
        zns = tp.data.extract.extract_slice((0.25,0.25,0), (1,1,0),
            mode=ExtractMode.OneZonePerConnectedRegion)
        self.assertEqual(ds.num_zones, 5)
        self.assertEqual(len(zns), 2)
        self.assertIsInstance(zns[0], tp.data.zone.Zone)
        self.assertIsInstance(zns[1], tp.data.zone.Zone)


if __name__ == '__main__':
    from .. import main
    main()
