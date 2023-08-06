from ..tecutil import _tecutil, sv
from ..constant import *
from ..exception import *
from .. import tecutil

from .animation import animation
from .export_setup import ExportSetup
from .print_setup import PrintSetup


@tecutil.lock()
def save_time_animation(filename, start_time=None, end_time=None,
                        timestep_step=1, width=800, animation_speed=10,
                        region=ExportRegion.AllFrames, supersample=3,
                        compression=None, image_type=None,
                        multiple_color_tables=False, format_options=None,
                        format=None):
    ani = animation(filename=filename, width=width,
                    animation_speed=animation_speed, region=region,
                    supersample=supersample, compression=compression,
                    image_type=image_type,
                    multiple_color_tables=multiple_color_tables,
                    format_options=format_options, format=format)
    ani.setup()
    with tecutil.ArgList() as arglist:
        if start_time is not None:
            arglist[sv.STARTTIME] = float(start_time)
        if end_time is not None:
            arglist[sv.ENDTIME] = float(end_time)
        if timestep_step is not None:
            arglist[sv.SKIP] = int(timestep_step)
        arglist[sv.CREATEMOVIEFILE] = True
        if not _tecutil.AnimateTimeX(arglist):
            raise TecplotSystemError()


def save_time_animation_avi(filename, start_time=None, end_time=None,
                            timestep_step=1, width=800, animation_speed=10,
                            region=ExportRegion.AllFrames, supersample=3,
                            compression=None, multiple_color_tables=False):
    """Export transient data time-series AVI animation to a file.

    Parameters:
        filename (`str`): The resulting video file name or path, relative to
            Python's current working directory.
        start_time (`float`, optional): The beginning solution time of the
            animation. This defaults to the earliest solution time in the
            dataset.
        end_time (`float`, optional): The ending solution time of the
            animation. This defaults to the latest solution time in the
            dataset.
        timestep_step (`int`, optional): The number of timesteps to increments
            for each frame of the animation. (default: 1)
        width (`int`, optional): The width of the video in pixels. (default:
            800)
        animation_speed (`int`, optional): The frame-rate of the video in
            frames per second. (default: 10)
        region (`Frame` or `ExportRegion`, optional): The rectangular area to
            be exported. This can be a specific `Frame` object or one of
            `ExportRegion.CurrentFrame`, `ExportRegion.AllFrames` (default) or
            `ExportRegion.WorkArea`.
        supersample (`int`, optional): Controls the amount of anti-aliasing
            used in each frame. Valid values are 1-16. A value of **1**
            indicates that no antialiasing will be used. Antialiasing smooths
            jagged edges on text, lines, and edges of the video output by the
            process of supersampling. *Some graphics cards* can cause Tecplot
            360 to crash when larger anti-aliasing values are used. If this
            occurs on your machine, try updating your graphics driver or using
            a lower anti-aliasing value. (default: **3**)
        compression (`AVICompression`, optional): The compression scheme to use
            when creating the video stream. Options are:
            `AVICompression.ColorPreserving` (default on Windows),
            `AVICompression.LinePreserving` or
            `AVICompression.LosslessUncompressed` (default on Linux and MacOS).
        multiple_color_tables (`bool`, optional): Create a color table for each
            frame of the animation. If `False` (default), the whole animation
            will be scanned in an attempt to create a single table of 256
            colors.

    Example usage, see the example under `save_time_animation_mpeg4` for a
    complete working example::

        >>> tp.export.save_time_animation_avi('output.avi')
    """
    return save_time_animation(filename=filename, start_time=start_time,
                               end_time=end_time, timestep_step=timestep_step,
                               width=width, animation_speed=animation_speed,
                               region=region, supersample=supersample,
                               compression=compression,
                               multiple_color_tables=multiple_color_tables,
                               format=ExportFormat.AVI)


def save_time_animation_flash(filename, start_time=None, end_time=None,
                              timestep_step=1, width=800, animation_speed=10,
                              region=ExportRegion.AllFrames, supersample=3,
                              compression=None,
                              image_type=FlashImageType.Lossless):
    """Export transient data time-series Flash animation to a file.

    Parameters:
        filename (`str`): The resulting video file name or path, relative to
            Python's current working directory.
        start_time (`float`, optional): The beginning solution time of the
            animation. This defaults to the earliest solution time in the
            dataset.
        end_time (`float`, optional): The ending solution time of the
            animation. This defaults to the latest solution time in the
            dataset.
        timestep_step (`int`, optional): The number of timesteps to increments
            for each frame of the animation. (default: 1)
        width (`int`, optional): The width of the video in pixels. (default:
            800)
        animation_speed (`int`, optional): The frame-rate of the video in
            frames per second. (default: 10)
        region (`Frame` or `ExportRegion`, optional): The rectangular area to
            be exported. This can be a specific `Frame` object or one of
            `ExportRegion.CurrentFrame`, `ExportRegion.AllFrames` (default) or
            `ExportRegion.WorkArea`.
        supersample (`int`, optional): Controls the amount of anti-aliasing
            used in each frame. Valid values are 1-16. A value of **1**
            indicates that no antialiasing will be used. Antialiasing smooths
            jagged edges on text, lines, and edges of the video output by the
            process of supersampling. *Some graphics cards* can cause Tecplot
            360 to crash when larger anti-aliasing values are used. If this
            occurs on your machine, try updating your graphics driver or using
            a lower anti-aliasing value. (default: **3**)
        compression (`FlashCompressionType`, optional): The compression scheme
            to use when creating the video stream. Options are:
            `FlashCompressionType.BestSpeed` (default) and
            `FlashCompressionType.SmallestSize`.
        image_type (`FlashImageType`, optional): The type of images to generate
            for each frame of the animation. Options are:
            `FlashImageType.Color256`, `FlashImageType.JPEG` and
            `FlashImageType.Lossless` (default).

    Example usage, see the example under `save_time_animation_mpeg4` for a
    complete working example::

        >>> tp.export.save_time_animation_flash('output.flv')
    """
    save_time_animation(filename=filename, start_time=start_time,
                        end_time=end_time, timestep_step=timestep_step,
                        width=width, animation_speed=animation_speed,
                        region=region, supersample=supersample,
                        compression=compression, image_type=image_type,
                        format=ExportFormat.Flash)


def save_time_animation_mpeg4(filename, start_time=None, end_time=None,
                              timestep_step=1, width=800, animation_speed=10,
                              region=ExportRegion.AllFrames, supersample=3,
                              format_options=None
):
    """Export transient data time-series MPEG-4 animation to a file.

    Parameters:
        filename (`str`): The resulting video file name or path, relative to
            Python's current working directory.
        start_time (`float`, optional): The beginning solution time of the
            animation. This defaults to the earliest solution time in the
            dataset.
        end_time (`float`, optional): The ending solution time of the
            animation. This defaults to the latest solution time in the
            dataset.
        timestep_step (`int`, optional): The number of timesteps to increments
            for each frame of the animation. (default: 1)
        width (`int`, optional): The width of the video in pixels. (default:
            800)
        animation_speed (`int`, optional): The frame-rate of the video in
            frames per second. (default: 10)
        region (`Frame` or `ExportRegion`, optional): The rectangular area to
            be exported. This can be a specific `Frame` object or one of
            `ExportRegion.CurrentFrame`, `ExportRegion.AllFrames` (default) or
            `ExportRegion.WorkArea`.
        supersample (`int`, optional): Controls the amount of anti-aliasing
            used in each frame. Valid values are 1-16. A value of **1**
            indicates that no antialiasing will be used. Antialiasing smooths
            jagged edges on text, lines, and edges of the video output by the
            process of supersampling. *Some graphics cards* can cause Tecplot
            360 to crash when larger anti-aliasing values are used. If this
            occurs on your machine, try updating your graphics driver or using
            a lower anti-aliasing value. (default: **3**)
        format_options (`str`, optional): A string of options passed directly
            to the underlying application `FFmpeg <https://www.ffmpeg.org/>`_.
            By default, this will be "-c:v libx264 -profile:v high -crf 20
            -pix_fmt yuv420p".

    Example usage:

    .. code-block:: python
        :emphasize-lines: 19-21

        import os

        import tecplot as tp
        from tecplot.constant import *

        examples = tp.session.tecplot_examples_directory()
        datafile = os.path.join(examples, 'SimpleData', 'VortexShedding.plt')
        dataset = tp.data.load_tecplot(datafile)

        plot = tp.active_frame().plot(PlotType.Cartesian2D)
        plot.activate()
        plot.show_contour = True

        plot.axes.x_axis.min = -0.002
        plot.axes.x_axis.max = 0.012
        plot.axes.y_axis.min = -0.006
        plot.axes.y_axis.max = 0.006

        tp.export.save_time_animation_mpeg4('vortex_shedding.mp4',
                                            start_time=0, end_time=0.0006,
                                            width=400, supersample=3)

    .. raw:: html

        <video controls>
            <source src="../_static/videos/vortex_shedding.m4v" type="video/mp4">
            I'm sorry; your browser doesn't support HTML5 MPEG4/H.264 video.
        </video>
    """
    save_time_animation(filename=filename, start_time=start_time,
                        end_time=end_time, timestep_step=timestep_step,
                        width=width, animation_speed=animation_speed,
                        region=region, supersample=supersample,
                        format_options=format_options,
                        format=ExportFormat.MPEG4)


def save_time_animation_raster_metafile(filename, start_time=None,
                                        end_time=None, timestep_step=1,
                                        width=800, animation_speed=10,
                                        region=ExportRegion.AllFrames,
                                        supersample=3,
                                        multiple_color_tables=False):
    """Export transient data time-series Raster Metafile animation to a file.

    Parameters:
        filename (`str`): The resulting video file name or path, relative to
            Python's current working directory.
        start_time (`float`, optional): The beginning solution time of the
            animation. This defaults to the earliest solution time in the
            dataset.
        end_time (`float`, optional): The ending solution time of the
            animation. This defaults to the latest solution time in the
            dataset.
        timestep_step (`int`, optional): The number of timesteps to increments
            for each frame of the animation. (default: 1)
        width (`int`, optional): The width of the video in pixels. (default:
            800)
        animation_speed (`int`, optional): The frame-rate of the video in
            frames per second. (default: 10)
        region (`Frame` or `ExportRegion`, optional): The rectangular area to
            be exported. This can be a specific `Frame` object or one of
            `ExportRegion.CurrentFrame`, `ExportRegion.AllFrames` (default) or
            `ExportRegion.WorkArea`.
        supersample (`int`, optional): Controls the amount of anti-aliasing
            used in each frame. Valid values are 1-16. A value of **1**
            indicates that no antialiasing will be used. Antialiasing smooths
            jagged edges on text, lines, and edges of the video output by the
            process of supersampling. *Some graphics cards* can cause Tecplot
            360 to crash when larger anti-aliasing values are used. If this
            occurs on your machine, try updating your graphics driver or using
            a lower anti-aliasing value. (default: **3**)
        multiple_color_tables (`bool`, optional): Create a color table for each
            frame of the animation. If `False` (default), the whole animation
            will be scanned in an attempt to create a single table of 256
            colors.

    Example usage, see the example under `save_time_animation_mpeg4` for a
    complete working example::

        >>> tp.export.save_time_animation_raster_metafile('output.rm')
    """
    save_time_animation(filename=filename, start_time=start_time,
                        end_time=end_time, timestep_step=timestep_step,
                        width=width, animation_speed=animation_speed,
                        region=region, supersample=supersample,
                        multiple_color_tables=multiple_color_tables,
                        format=ExportFormat.RasterMetafile)


def save_time_animation_wmv(filename, start_time=None, end_time=None,
                            timestep_step=1, width=800, animation_speed=10,
                            region=ExportRegion.AllFrames, supersample=3,
                            format_options=None):
    """Export transient data time-series Windows Media Video (WMV) to a file.

    Parameters:
        filename (`str`): The resulting video file name or path, relative to
            Python's current working directory.
        start_time (`float`, optional): The beginning solution time of the
            animation. This defaults to the earliest solution time in the
            dataset.
        end_time (`float`, optional): The ending solution time of the
            animation. This defaults to the latest solution time in the
            dataset.
        timestep_step (`int`, optional): The number of timesteps to increments
            for each frame of the animation. (default: 1)
        width (`int`, optional): The width of the video in pixels. (default:
            800)
        animation_speed (`int`, optional): The frame-rate of the video in
            frames per second. (default: 10)
        region (`Frame` or `ExportRegion`, optional): The rectangular area to
            be exported. This can be a specific `Frame` object or one of
            `ExportRegion.CurrentFrame`, `ExportRegion.AllFrames` (default) or
            `ExportRegion.WorkArea`.
        supersample (`int`, optional): Controls the amount of anti-aliasing
            used in each frame. Valid values are 1-16. A value of **1**
            indicates that no antialiasing will be used. Antialiasing smooths
            jagged edges on text, lines, and edges of the video output by the
            process of supersampling. *Some graphics cards* can cause Tecplot
            360 to crash when larger anti-aliasing values are used. If this
            occurs on your machine, try updating your graphics driver or using
            a lower anti-aliasing value. (default: **3**)
        format_options (`str`, optional): A string of options passed directly
            to the underlying application `FFmpeg <https://www.ffmpeg.org/>`_.
            By default, this will be "-qscale 4".

    Example usage, see the example under `save_time_animation_mpeg4` for a
    complete working example::

        >>> tp.export.save_time_animation_wmv('output.wmv')
    """
    save_time_animation(filename=filename, start_time=start_time,
                        end_time=end_time, timestep_step=timestep_step,
                        width=width, animation_speed=animation_speed,
                        region=region, supersample=supersample,
                        format_options=format_options, format=ExportFormat.WMV)
