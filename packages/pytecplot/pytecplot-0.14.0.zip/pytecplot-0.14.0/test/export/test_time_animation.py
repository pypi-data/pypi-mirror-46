import os
import unittest
from unittest.mock import *

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

from ..sample_data import sample_data
from .. import (patch_tecutil, closed_tempfile, skip_if_sdk_version_before,
                mocked_sdk_version)
from .test_animation import isvideo


class TestTimeAnimation(unittest.TestCase):
    _OPTS = dict(width=32, supersample=1)

    def setUp(self):
        tp.new_layout()
        self.filename, _ = sample_data('3x3x3_3zones_time')
        tp.active_frame().plot(PlotType.Cartesian3D).activate()

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    def test_animation_avi(self):
        with closed_tempfile('.avi') as fname:
            tp.export.save_time_animation_avi(fname, **TestTimeAnimation._OPTS)
            self.assertTrue(isvideo(fname))

    def test_mpeg4_failure_on_out_of_date_engine(self):
        with mocked_sdk_version(2017, 2):
            with closed_tempfile('.avi') as fname:
                tp.export.save_time_animation_avi(fname, **TestTimeAnimation._OPTS)
                self.assertTrue(isvideo(fname))
            with self.assertRaises(TecplotOutOfDateEngineError):
                with closed_tempfile('.mp4') as fname:
                    tp.export.save_time_animation(fname, **TestTimeAnimation._OPTS)

    @skip_if_sdk_version_before(2017, 3)
    def test_animation_mpeg4(self):
        opts = TestTimeAnimation._OPTS.copy()
        opts.update(
            start_time = 1,
            end_time = 2,
            timestep_step = 1,
        )
        with closed_tempfile('.mp4') as fname:
            tp.export.save_time_animation_mpeg4(fname, **opts)
            self.assertTrue(isvideo(fname))

    @skip_if_sdk_version_before(2017, 3)
    def test_animation_mpeg4_byext(self):
        with closed_tempfile('.mp4') as fname:
            tp.export.save_time_animation(fname, **TestTimeAnimation._OPTS)
            self.assertTrue(isvideo(fname))

    @skip_if_sdk_version_before(2017, 3)
    def test_animation_wmv(self):
        with closed_tempfile('.wmv') as fname:
            tp.export.save_time_animation_wmv(fname, **TestTimeAnimation._OPTS)
            self.assertTrue(isvideo(fname))

    def test_animation_raster_metafile(self):
        with closed_tempfile('.rm') as fname:
            tp.export.save_time_animation_raster_metafile(fname, **TestTimeAnimation._OPTS)
            # no good way to determine video format for
            # raster metafiles so just check the file size
            with open(fname, 'rb') as fin:
                self.assertGreater(len(fin.read()), 800)

    def test_animation_flash(self):
        with closed_tempfile('.flv') as fname:
            opts = TestTimeAnimation._OPTS.copy()
            opts.update(
                compression = FlashCompressionType.SmallestSize,
                image_type = FlashImageType.Color256
            )
            tp.export.save_time_animation_flash(fname, **opts)
            self.assertTrue(isvideo(fname))

    @skip_if_sdk_version_before(2017, 3)
    def test_failures(self):
        with closed_tempfile('.mp4') as fname:
            with patch_tecutil('AnimateTimeX', return_value=False):
                with self.assertRaises(TecplotSystemError):
                    tp.export.save_time_animation_mpeg4(fname)


if __name__ == '__main__':
    from .. import main
    main()

