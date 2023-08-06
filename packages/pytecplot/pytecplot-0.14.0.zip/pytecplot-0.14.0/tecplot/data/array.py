from builtins import range, super

import logging
import textwrap

from ctypes import (addressof, byref, cast, c_double, c_float, c_int8, c_int16,
                    c_int32, c_int64, c_void_p, POINTER)

from ..tecutil import _tecutil, _tecutil_connector
from ..constant import *
from ..exception import *
from .. import session
from ..tecutil import lock, lock_attributes

log = logging.getLogger(__name__)


class Array(c_void_p):
    """Low-level accessor for underlying data within a `Dataset`.

    .. note::

        The data manipulation context referred to below is currently being
        developed and should show up in an up-coming revision.

    This object exposes a list-like interface to the underlying data array.
    Using it, values can be directly queried and modified. After any
    modification to the data, the Tecplot Engine will have to be notified of
    the change. This notification will happen automatically in most cases, but
    can be turned off using the data manipulation context for a significant
    performance increase on large datasets.

    Accessing values within an `Array` is done through the standard ``[]``
    syntax::

        >>> print(array[3])
        3.1415

    The numbers passed are interpreted just like Python's built-in
    :py:class:`slice` object::

        >>> # print the values at indices: 5, 7, 9
        >>> print(array[5:10:2])
        [1.0, 1.0, 1.0]

    Elements within an array can be manipulated in-place with the assignment
    operator::

        >>> array[3] = 5.0
        >>> print(array[3])
        5.0

    Element-by-element access is *not* guaranteed to be performant and users
    should avoid writing loops over indices in Python. Instead, whole arrays
    should be used. This will effectively push the loop down to the underlying
    native library and will be much faster in virtually all cases.

    Consider this array of 10k elements::

        >>> ds = frame.create_dataset('Dataset', ['x'])
        >>> zn = ds.add_ordered_zone('Zone', 10000)
        >>> array = zn.values('x')

    The following loop, which takes the sine of all values in the array will
    require several Python function calls per element which is a tremendous
    overhead::

        >>> import math
        >>> for i in range(len(ar)):
        ...     ar[i] = math.sin(ar[i])

    An immediate improvement on this can be made by looping over the elements
    in Python only when reading the values, but assigning them using the
    whole array. This will be several times faster for even modest arrays::

        >>> ar[:] = [math.sin(x) for x in ar]

    But there is still a large performance penalty for looping over elements
    directly in Python and PyTecplot supports two solutions for large arrays:
    `tecplot.data.operate.execute_equation` and `tecplot.extension.numpy`.
    Please refer to these for details. Continuing with the example above, we
    could accomplish the same thing with either of the following using
    `execute_equation` (assuming the array is identified by the first zone,
    first variable)::

        >>> from tecplot.data.operate import execute_equation
        >>> execute_equation('V1 = SIN(V1)', zones=[dataset.zone(0)])

    or by using the `numpy` library::

        >>> import numpy as np
        >>> ar[:] = np.sin(ar[:])

    In both of these cases, the calculation of the sine and loop over elements
    is pushed to the low level library and is much faster.
    """
    def __init__(self, zone, variable):
        self.zone = zone
        self.variable = variable
        super().__init__(self._native_reference())

    @property
    def _cache(self):
        if _tecutil_connector.suspended:
            _tecutil_connector._delete_caches.append(self._delete_cache)
            return True
        else:
            return False

    def _delete_cache(self):
        attrs = '''
            _rnr _wnr _rrp _wrp
            _location
            _len
            _data_type
        '''.split()
        for attr in attrs:
            try:
                delattr(self, attr)
            except AttributeError:
                pass

    def _native_reference(self, writable=False):
        args = (self.zone.dataset.uid, self.zone.index + 1, self.variable.index + 1)
        if writable:
            if self._cache:
                if not hasattr(self, '_wnr'):
                    with lock():
                        self._wnr = _tecutil.DataValueGetWritableNativeRefByUniqueID(*args)
                return self._wnr
            else:
                with lock():
                    return _tecutil.DataValueGetWritableNativeRefByUniqueID(*args)
        else:
            if self._cache:
                if not hasattr(self, '_rnr'):
                    with lock():
                        self._rnr = _tecutil.DataValueGetReadableNativeRefByUniqueID(*args)
                return self._rnr
            else:
                with lock():
                    return _tecutil.DataValueGetReadableNativeRefByUniqueID(*args)

    @lock()
    def _raw_pointer(self, writable=False):
        if _tecutil_connector.connected:
            msg = 'raw pointer access only available in batch-mode'
            raise TecplotLogicError(msg)
        elif writable:
            ref = self._native_reference(writable=True)
            _tecutil.handle.tecUtilDataValueGetWritableRawPtrByRef.restype = \
                POINTER(self.c_type)
            wrp = _tecutil.DataValueGetWritableRawPtrByRef(ref)
            if self._cache:
                if not hasattr(self, '_wrp'):
                    self._wrp = wrp
                return self._wrp
            else:
                return wrp
        else:
            _tecutil.handle.tecUtilDataValueGetReadableRawPtrByRef.restype = \
                POINTER(self.c_type)
            rrp = _tecutil.DataValueGetReadableRawPtrByRef(self)
            if self._cache:
                if not hasattr(self, '_rrp'):
                    self._rrp = rrp
                return self._rrp
            else:
                return rrp

    def __eq__(self, other):
        self_addr = addressof(cast(self, POINTER(c_int64)).contents)
        other_addr = addressof(cast(other, POINTER(c_int64)).contents)
        return self_addr == other_addr

    def __ne__(self, other):
        return not (self == other)

    def __len__(self):
        """The number of values in this array.

        :rtype: `integer <int>`

        Example showing size of ordered data::

            >>> x = dataset.zone('Zone').values('X')
            >>> print(x.shape)
            (10, 10, 10)
            >>> print(len(x))
            1000
        """
        if self._cache:
            if not hasattr(self, '_len'):
                self._len = _tecutil.DataValueGetCountByRef(self)
            return self._len
        else:
            return _tecutil.DataValueGetCountByRef(self)

    @property
    def location(self):
        """`ValueLocation`: Data points location with respect to the elements.

        Possible values are `ValueLocation.CellCentered` and
        `ValueLocation.Nodal`. Example usage::

            >>> print(dataset.zone(0).values('X').location)
            ValueLocation.Nodal
        """
        if self._cache:
            if not hasattr(self, '_location'):
                self._location = _tecutil.DataValueGetLocation(
                    self.zone.index + 1, self.variable.index + 1)
            return self._location
        else:
            return _tecutil.DataValueGetLocation(self.zone.index + 1,
                                                 self.variable.index + 1)

    @property
    def shape(self):
        """`tuple` of `floats <float>`: ``(i, j, k)`` shape for this array.

        This is defined by the parent zone and can be used to reshape arrays.
        The following example assumes 32-bit floating point array and copies
        the Tecplot-owned ``data`` into the `numpy`-owned ``array``::

            >>> import numpy as np
            >>> data = dataset.zone('Zone').values('X')
            >>> array = np.empty(data.shape, dtype=np.float32)
            >>> arr_ptr = array.ctypes.data_as(POINTER(data.c_type))
            >>> memmove(arr_ptr, data.copy(), sizeof(data.c_type) * len(data))

        The data array presented is normally one-dimensional. For ordered data,
        you may wish to reshape the array indexing according to the
        dimensionality given by the ``shape`` attribute:

        .. code-block:: python
            :emphasize-lines: 30

            import numpy as np
            import tecplot as tp

            frame = tp.active_frame()
            dataset = frame.create_dataset('Dataset', ['X'])
            zone = dataset.add_ordered_zone('Zone', shape=(3,3,3))

            '''
            the following will print:
            [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
              0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
            '''
            x = np.array(zone.values('X')[:])
            print(x)

            '''
            the following will print:
            [[[ 0.  0.  0.]
              [ 0.  0.  0.]
              [ 0.  0.  0.]]

             [[ 0.  0.  0.]
              [ 0.  0.  0.]
              [ 0.  0.  0.]]

             [[ 0.  0.  0.]
              [ 0.  0.  0.]
              [ 0.  0.  0.]]]
            '''
            x.shape = zone.values('X').shape
            print(x)

        """
        if self.zone.zone_type is ZoneType.Ordered:
            array_shape = tuple(i for i in self.zone._shape if i > 1)
        else:
            array_shape = (self.zone.num_points,)
        if self.location is ValueLocation.CellCentered:
            array_shape = tuple(i - 1 for i in array_shape if i > 2)
        if not array_shape:
            array_shape = (1,)
        return array_shape

    @property
    def c_type(self):
        """`ctypes` compatible data type of this array.

        This is the `ctypes` equivalent of `Array.data_type` and will return
        one of the following:

            * `ctypes.c_float`
            * `ctypes.c_double`
            * `ctypes.c_int`
            * `ctypes.c_int16`
            * `ctypes.c_int8`

        and can be used to create a `ctypes` array to store a copy of the
        data:

        .. code-block:: python

            import tecplot as tp
            frame = tp.active_frame()
            dataset = frame.create_dataset('Dataset', ['x'])
            dataset.add_ordered_zone('Zone', (3,3,3))
            x = dataset.zone('Zone').values('x')
            # allocate array using Python's ctypes
            x_array = (x.c_type * len(x))()
            # copy values from Dataset into ctypes array
            x_array[:] = x[:]
        """
        _ctypes = {
            FieldDataType.Float: c_float,
            FieldDataType.Double: c_double,
            FieldDataType.Int32: c_int32,
            FieldDataType.Int16: c_int16,
            FieldDataType.Byte: c_int8}
        return _ctypes[self.data_type]

    @property
    def data_type(self):
        """`FieldDataType`: Indicating the underlying value type of this array.

        Example usage::

            >>> print(dataset.zone('Zone').values('X').data_type)
            FieldDataType.Float
        """
        return _tecutil.DataValueGetRefType(self)

    @lock()
    def copy(self, offset=0, size=None):
        """Copy the whole or part of the array into a ctypes array.

        Parameters:
            offset (`int`, optional): Zero-based offset for starting
                index to copy. (default: 0)
            size (`int`, optional): Number of values to copy into the
                resulting array. A value of `None` will copy to the end of the
                array. (default: `None`)

        Here we will copy out chunks of the data, do some operation and set the
        values back into the dataset:

        .. code-block:: python

            import tecplot as tp

            tp.new_layout()
            frame = tp.active_frame()
            dataset = frame.create_dataset('Dataset', ['x'])
            dataset.add_ordered_zone('Zone', (2, 2, 2))
            x = dataset.zone('Zone').values('x')

            # loop over array copying out 4 values at a time
            for i, offset in enumerate(range(0, len(x), 4)):
                x_array = x.copy(offset, 4)
                x_array[:] = [i] * 4
                x[offset:offset + 4] = x_array

            # will print: [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]
            print(x[:])
        """
        size = (len(self) - offset) if size is None else size
        arr = (self.c_type * size)()
        _tecutil.DataValueArrayGetByRef(self, offset + 1, size, arr)
        return arr

    def _slice_range(self, s):
        start = s.start or 0
        stop = s.stop or len(self)
        step = s.step or 1
        return range(start, stop, step)

    def __getitem__(self, i):
        if _tecutil_connector.connected:
            if isinstance(i, slice):
                s = self._slice_range(i)
                if s.step == 1:
                    n = s.stop - s.start
                    return self.copy(s.start, n)[:]
                else:
                    return [_tecutil.DataValueGetByRef(self, ii + 1)
                            for ii in s]
            else:
                return _tecutil.DataValueGetByRef(self, i + 1)
        else:
            if isinstance(i, slice):
                data = self._raw_pointer()
                return [data[ii] for ii in self._slice_range(i)]
            else:
                return self._raw_pointer()[i]

    def __setitem__(self, i, val):
        index = None
        if _tecutil_connector.connected:
            ref = self._native_reference(writable=True)
            if isinstance(i, slice):
                s = self._slice_range(i)
                if s.step == 1:
                    n = s.stop - s.start
                    try:
                        import numpy as np
                        data_ctype = self.c_type
                        nparr = np.asarray(val, dtype=data_ctype)
                        ptarr = nparr.ctypes.data_as(POINTER(data_ctype))
                        arr = (data_ctype * n).from_address(addressof(ptarr.contents))
                    except ImportError:
                        msg = textwrap.dedent('''\
                            Falling back to using basic Python for data operations.
                            If installed, PyTecplot will make use of Numpy where
                            appropriate for significant perfomance gains.
                        ''')
                        log.warning(msg)
                        arr = (self.c_type * n)(*val)
                    _tecutil.DataValueArraySetByRef(ref, s.start + 1, n, arr)
                else:
                    for ival, ii in enumerate(s):
                        _tecutil.DataValueSetByRef(ref, ii + 1, val[ival])
            else:
                _tecutil.DataValueSetByRef(ref, i + 1, val)
                index = i + 1
        else:
            if isinstance(i, slice):
                s = self._slice_range(i)
                if len(s) != len(val):
                    raise TecplotIndexError('Array length mismatch {} != {}'.format(len(s), len(val)))
                data = self._raw_pointer(True)
                try:
                    import numpy as np
                    data_ctype = self.c_type
                    nparr = np.frombuffer((data_ctype * len(self)).from_address(addressof(data.contents)), data_ctype)
                    nparr[i] = val
                except ImportError:
                    msg = textwrap.dedent('''\
                        Falling back to using basic Python for data operations.
                        If installed, PyTecplot will make use of Numpy where
                        appropriate for significant perfomance gains.
                    ''')
                    log.warning(msg)
                    for ival, ii in enumerate(self._slice_range(i)):
                        data[ii] = val[ival]
            else:
                self._raw_pointer(True)[i] = val
                index = i + 1
        session.data_altered(self.zone, self.variable, index)

    def __iter__(self):
        self.current_index = -1
        self.current_length = len(self)
        return self

    def __next__(self):
        self.current_index += 1
        if self.current_index < self.current_length:
            return self.__getitem__(self.current_index)
        else:
            del self.current_index
            del self.current_length
            raise StopIteration

    def next(self):  # if sys.version_info < (3,)
        return self.__next__()

    def minmax(self):
        """Limits of the values stored in this array.

        :rtype: `tuple` of `floats <float>`

        This always returns `floats <float>` regardless of the underlying data
        type::

            >>> print(dataset.zone('Zone').values('x').minmax())
            (0, 10)
        """
        return _tecutil.DataValueGetMinMaxByRef(self)

    def min(self):
        """Lower bound of the values stored in this array.

        :rtype: `float`

        This always returns a `float` regardless of the underlying data type::

            >>> print(dataset.zone('Zone').values('x').min())
            0
        """
        return self.minmax()[0]

    def max(self):
        """Upper bound of the values stored in this array.

        :rtype: `float`

        This always returns a `float` regardless of the underlying data type::

            >>> print(dataset.zone('Zone').values('x').max())
            10
        """
        return self.minmax()[1]

    @property
    def shared_zones(self):
        """`list` of `Zones <data_access>`: All `Zones <data_access>` sharing this array.

        Example usage::

            >>> dataset.zone('My Zone').copy(share_variables=True)
            >>> for z in dataset.zone('My Zone').values(0).shared_zones:
            ...     print(z.index)
            0
            1
        """
        indices = _tecutil.DataValueGetShareZoneSet(self.zone.index + 1,
                                                    self.variable.index + 1)
        ret = [self.zone.dataset.zone(i) for i in indices]
        indices.dealloc()
        return ret

    @property
    def passive(self):
        """`bool`: An unallocated zone-variable combination.

        Passive variables are placeholders where no data is defined for a zone
        variable combination. Passive variables will always return zero when
        queried:

        .. code-block:: python

            import tecplot as tp

            ds = tp.active_page().add_frame().create_dataset('D', ['x','y'])
            z = ds.add_ordered_zone('Z1', (3,))
            assert not z.values(0).passive
        """
        return _tecutil.DataValueIsPassive(self.zone.index + 1,
                                           self.variable.index + 1)
