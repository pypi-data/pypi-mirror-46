import ctypes

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import layout, tecutil, version
from ..tecutil import sv


@tecutil.lock()
def extract_line(points, num_points=None, frame=None, dataset=None):
    """Create new zone from a line in the dataset.

    Parameters:
        points (``2D numeric array``): The points defining the line in two or
            three dimensions. This array must be of the shape *(N, D)* where
            *N* is the number points and *D* is the number of dimensions. That
            is, it must take the form ``[(x0, y0, z0), (x1, y1, z1) ...]``.
            Points that do not lie within the dataset volume will be removed
            from the resulting zone.
        num_points (`int`, optional): The number of points to evenly
            distribute along the polyline. (default: length of *points* or *N*)
        frame (`Frame`, optional): A `Frame` that holds the `Dataset` to
            operate on which must match *dataset* if given. (default: currently
            active `Frame`)
        dataset (`Dataset`, optional): The `Dataset` to operate on which must
            be attached to *frame* if given. (default: currently active
            `Dataset`)

    Returns:
        A 1D `OrderedZone` representing a line through the data. Points outside
        of the dataset will be removed from the extracted zone resulting in
        fewer points than input.

    .. warning::

        Line extraction is only available when the plot type is set to
        `Cartesian2D` or `Cartesian3D`::

            >>> from tecplot.constant import PlotType
            >>> frame.plot_type = PlotType.Cartesian3D

    This example shows how to extract a zone along a line, overlaying the
    result in a new frame:

    .. code-block:: python
        :emphasize-lines: 26

        import numpy as np
        from os import path

        import tecplot as tp
        from tecplot.constant import *

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = path.join(examples_dir, 'SimpleData', 'VortexShedding.plt')
        dataset = tp.data.load_tecplot(datafile)

        frame = tp.active_frame()
        frame.activate()
        plot = frame.plot()
        plot.contour(0).variable = dataset.variable("P(N/M2)")
        plot.show_contour = True
        plot.contour(0).levels.reset(num_levels=11)
        plot.contour(0).colormap_name = 'Sequential - Yellow/Green/Blue'

        plot.axes.y_axis.min = -0.01
        plot.axes.y_axis.max = 0.01
        plot.axes.x_axis.min = -0.005
        plot.axes.x_axis.max = 0.015

        xx = np.linspace(0, 0.01, 100)
        yy = np.zeros(100)
        line = tp.data.extract.extract_line(zip(xx, yy))

        plot.show_mesh = True
        plot.fieldmap(0).mesh.show = False

        frame = tp.active_page().add_frame()
        frame.position = (3.0, 0.5)
        frame.height = 2
        frame.width = 4
        plot = tp.active_frame().plot(PlotType.XYLine)
        plot.activate()

        plot.delete_linemaps()
        lmap = plot.add_linemap('data', line, x=dataset.variable('P(N/M2)'),
                                y=dataset.variable('T(K)'))
        lmap.line.line_thickness = 2.0
        plot.axes.x_axis(0).title.font.size = 10
        plot.axes.y_axis(0).title.font.size = 10
        plot.axes.viewport.left = 20
        plot.axes.viewport.bottom = 20
        plot.view.fit()

        tp.export.save_png("extract_line.png", region=ExportRegion.AllFrames,
                           width=600, supersample=3)

    .. figure:: /_static/images/extract_line.png
        :width: 300px
        :figwidth: 300px
    """
    if dataset is None:
        if frame is None:
            frame = layout.active_frame()
        dataset = frame.dataset
    elif frame is None:
        frame = dataset.frame

    if __debug__:
        if frame.plot_type not in [PlotType.Cartesian2D, PlotType.Cartesian3D]:
            msg = 'must be in a cartesian plot type to extract a line'
            raise TecplotLogicError(msg)
        if dataset != frame.dataset:
            msg = 'dataset is not attached to given frame'
            raise TecplotLogicError(msg)

    new_zone_index = dataset.num_zones

    try:
        _ = points[0]
    except TypeError:
        points = list(points)

    ndim = len(points[0])
    if num_points is None:
        num_points = len(points)

    n = len(points)
    xx = (ctypes.c_double * n)(*(float(p[0]) for p in points))
    yy = (ctypes.c_double * n)(*(float(p[1]) for p in points))
    zz = (ctypes.c_double * n)(*([0.]*len(xx)
                                 if ndim < 3
                                 else (float(p[2]) for p in points)))

    extract_through_volume = ndim == 3
    only_points_on_line = num_points == len(points)
    include_distance = False
    to_file = False
    filename = None

    try:
        if not _tecutil.ExtractFromPolyline(xx, yy, zz, len(xx),
                                            extract_through_volume,
                                            only_points_on_line,
                                            include_distance, num_points,
                                            to_file, filename):
            raise TecplotSystemError()
    except TecplotLogicError as e:
        # If some of the points are outside of the data, the zone
        # is still extracted and this exception is not technically
        # an error. A different message is generated if all of the
        # points are outside of the data which is re-raised.
        if 'Probe Position is outside of the data' not in str(e):
            raise

    return dataset.zone(new_zone_index)


@tecutil.lock()
def extract_slice(origin=(0, 0, 0), normal=(0, 0, 1), source=None, mode=None,
                  copy_cell_centers=None, assign_strand_ids=None, frame=None,
                  dataset=None, **kw):
    """Create new zone from a plane in the dataset.

    Parameters:
        origin (array of three `floats <float>`): Point in space,
            :math:`(x, y, z)`, that lies on the slice plane.
        normal (array of three `floats <float>`): Vector direction,
            :math:`(x, y, z)`, indicating the normal of the slice plane.
        source (`SliceSource`): Source zone types to consider when extracting
            the slice. Possible values: `SliceSource.LinearZones`,
            `SliceSource.SurfaceZones`, `SliceSource.SurfacesOfVolumeZones`,
            `SliceSource.VolumeZones` (default).
        mode (`ExtractMode`): Controls how many zones are created. Possible
            values are: `ExtractMode.SingleZone` (default),
            `ExtractMode.OneZonePerConnectedRegion` and
            `ExtractMode.OneZonePerSourceZone`.
        copy_cell_centers (`bool`): If `True`, cell-center
            values will be copied when possible to the extracted slice plane.
            Cell-centers are copied when a variable is cell-centered for all
            the source zones through which the slice passes. Otherwise,
            extracted planes use node-centered data, which is calculated by
            interpolation. (default: `False`)
        assign_strand_ids (`bool`): automatically assign strand IDs
            to the data extracted from transient sources. This is only
            available if *multiple_zones* is `False`. (default: `True`)
        frame (`Frame`, optional): A `Frame` that holds the `Dataset` to
            operate on which must match *dataset* if given. (default: currently
            active `Frame`)
        dataset (`Dataset`, optional): The `Dataset` to operate on which must
            be attached to *frame* if given. (default: currently active
            `Dataset`)

    Returns:
        One or a `list` of `Zones <data_access>` representing a planar slice.

    .. warning::

        Slicing is only available when the plot type is set to 3D::

            >>> from tecplot.constant import PlotType
            >>> frame.plot_type = PlotType.Cartesian3D

    .. note::

        This function returns a list of zones if *mode* is set to
        `ExtractMode.OneZonePerConnectedRegion` or
        `ExtractMode.OneZonePerSourceZone` even if only one zone is created.
        Otherwise, a single zone is returned.

    .. seealso:: `tecplot.plot.SliceGroup.extract()`

    This example shows extracting a slice zone from the surface a wing:

    .. code-block:: python
        :emphasize-lines: 16-20

        import os
        import tecplot as tp
        from tecplot.constant import PlotType, SliceSource

        examples_dir = tp.session.tecplot_examples_directory()
        datafile = os.path.join(examples_dir, 'OneraM6wing',
                                'OneraM6_SU2_RANS.plt')
        dataset = tp.data.load_tecplot(datafile)

        frame = tp.active_frame()
        frame.plot_type = PlotType.Cartesian3D

        # set active plot to 3D and extract
        # an arbitrary slice from the surface
        # data on the wing
        extracted_slice = tp.data.extract.extract_slice(
            origin=(0, 0.25, 0),
            normal=(0, 1, 0),
            source=SliceSource.SurfaceZones,
            dataset=dataset)

        # switch plot type in current frame, clear plot
        plot = frame.plot(PlotType.XYLine)
        plot.activate()
        plot.delete_linemaps()

        # create line plot from extracted zone data
        cp_linemap = plot.add_linemap(
            name='Quarter-chord C_p',
            zone=extracted_slice,
            x=dataset.variable('x'),
            y=dataset.variable('Pressure_Coefficient'))

        # set style of linemap plot and
        # update axes limits to show data
        cp_linemap.line.color = tp.constant.Color.Blue
        cp_linemap.line.line_thickness = 0.8
        cp_linemap.y_axis.reverse = True
        plot.view.fit()

        # export image of pressure coefficient as a function of x
        tp.export.save_png('wing_slice_pressure_coeff.png', 600, supersample=3)

    .. figure:: /_static/images/wing_slice_pressure_coeff.png
        :width: 300px
        :figwidth: 300px
    """
    if 'multiple_zones' in kw:
        msg = '"multiple_zones" has been removed, please use "mode" instead'
        raise TecplotInterfaceChangeError(msg)
    if mode is not None and version.sdk_version_info < (2017, 3):
        msg = '"mode" parameter requires Tecplot 360 version 2017.3 or later'
        raise TecplotInterfaceChangeError(msg)

    if dataset is None:
        if frame is None:
            frame = layout.active_frame()
        dataset = frame.dataset
    elif frame is None:
        frame = dataset.frame

    if __debug__:
        if frame.dataset != dataset:
            raise TecplotLogicError('Dataset is not attached to frame.')
        if frame.plot_type is not PlotType.Cartesian3D:
            msg = 'Plot Type must be Cartesian3D to create a slice.'
            raise TecplotLogicError(msg)

    with frame.activated():
        new_zone_index = dataset.num_zones
        with tecutil.ArgList() as arglist:
            arglist[sv.ORIGINX] = float(origin[0])
            arglist[sv.ORIGINY] = float(origin[1])
            arglist[sv.ORIGINZ] = float(origin[2])
            arglist[sv.NORMALX] = float(normal[0])
            arglist[sv.NORMALY] = float(normal[1])
            arglist[sv.NORMALZ] = float(normal[2])
            if source is not None:
                arglist[sv.SLICESOURCE] = SliceSource(source)
            if mode is not None:
                arglist[sv.EXTRACTMODE] = ExtractMode(mode)
            arglist[sv.COPYCELLCENTEREDVALUES] = copy_cell_centers
            if assign_strand_ids is not None:
                arglist[sv.AUTOSTRANDTRANSIENTDATA] = bool(assign_strand_ids)
            if not _tecutil.CreateSliceZoneFromPlneX(arglist):
                raise TecplotSystemError()
            if dataset.num_zones == new_zone_index:
                raise TecplotLogicError('No zones found when extracting slice')
            if mode in [ExtractMode.OneZonePerConnectedRegion,
                        ExtractMode.OneZonePerSourceZone]:
                zone_indices = range(new_zone_index, dataset.num_zones)
                return [dataset.zone(i) for i in zone_indices]
            else:
                return dataset.zone(new_zone_index)


@tecutil.lock()
def extract_zones_from_connected_regions(zones):
    with tecutil.IndexSet(zones) as zone_set:
        if not _tecutil.ExtractZonesFromConnectedRegions(zone_set):
            raise TecplotSystemError()
