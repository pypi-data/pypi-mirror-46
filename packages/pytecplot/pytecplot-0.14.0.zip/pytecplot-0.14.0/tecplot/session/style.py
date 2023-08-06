from builtins import int, str

import ctypes
import logging

from ctypes import (c_char, c_char_p, c_double, c_size_t, c_int64, pointer,
                    POINTER)
from enum import Enum
from six import string_types

from ..tecutil import _tecutil, _tecutil_connector
from ..constant import *
from ..exception import *
from .. import tecutil, version
from ..tecutil import (Index, IndexRange, IndexSet, XYPosition, XYZPosition,
                       StringList, flatten_args, lock, lock_attributes,
                       maxuint64, minint64, sv)


log = logging.getLogger(__name__)


@lock(with_recording=False)
def set_style(value, *args, **kwargs):
    if __debug__:
        assert len(args) < 7, ', '.join(args)
        if isinstance(value, int):
            if value < minint64 or maxuint64 < value:
                raise TecplotOverflowError('Integer outside of valid range.')

        if log.getEffectiveLevel() < logging.INFO:
            msg = 'SetStyle\n'
            msg += '  value: {}\n'.format(value)
            for a in args:
                msg += '  {} {}\n'.format(type(a), a)
            for k, v in kwargs.items():
                msg += '  {} : {} {}\n'.format(k, type(v), v)
            log.debug(msg[:-1])

            _tecutil_connector._style_call_count['SET'][' '.join(args)] += 1

    if isinstance(value, IndexRange):
        args = list(args)
        imin, imax, istep = value
        imin = Index(imin or 0)
        imax = Index(imax or -1)
        istep = int(istep or 1)
        set_style(imin, *(args + [sv.MIN]), **kwargs)
        set_style(imax, *(args + [sv.MAX]), **kwargs)
        set_style(istep, *(args + [sv.SKIP]), **kwargs)
        return
    elif isinstance(value, XYPosition):
        args = list(args)
        for ax, val in zip([sv.X, sv.Y], value):
            if val is not None:
                set_style(float(val), *(args + [ax]), **kwargs)
        return
    elif isinstance(value, XYZPosition):
        args = list(args)
        for ax, val in zip([sv.X, sv.Y, sv.Z], value):
            if val is not None:
                set_style(float(val), *(args + [ax]), **kwargs)
        return

    with tecutil.ArgList() as arglist:

        allocd = []
        try:

            for i, p in enumerate(args):
                arglist[getattr(sv, 'P' + str(i + 1))] = p

            if isinstance(value, Enum):
                arglist[sv.IVALUE] = c_size_t(value.value)
            elif isinstance(value, Index):
                arglist[sv.IVALUE] = c_size_t(value + 1)
            elif isinstance(value, (int, bool)):
                arglist[sv.IVALUE] = c_size_t(value)
            elif isinstance(value, float):
                arglist[sv.DVALUE] = value
            elif isinstance(value, string_types):
                arglist[sv.STRVALUE] = value
            elif hasattr(value, '__iter__'):
                value_list = list(value)
                if not len(value_list) or isinstance(value_list[0], int):
                    value_obj = IndexSet(*value_list)
                    allocd.append(value_obj)
                    arglist[sv.IVALUE] = c_size_t(value_obj.value)
                else:
                    value_obj = StringList(*value_list)
                    allocd.append(value_obj)
                    arglist[sv.IVALUE] = c_size_t(ctypes.addressof(
                        ctypes.cast(value_obj, POINTER(c_size_t)).contents))
            else:
                raise TecplotTypeError

            for k, v in kwargs.items():
                k = k.upper()
                if k == sv.UNIQUEID:
                    v = c_size_t(v)
                elif k in [sv.OBJECTSET]:
                    v = IndexSet(*v)
                    allocd.append(v)
                elif k in [sv.OFFSET1, sv.OFFSET2]:
                    v = v + 1
                arglist[k] = v

            if __debug__:
                if log.getEffectiveLevel() < logging.INFO:
                    msg = 'SetStyle\n'
                    for k, v in arglist.items():
                        msg += '  {}: {}\n'.format(k, v)
                    log.debug(msg[:-1])

            try:
                res = _tecutil.StyleSetLowLevelX(arglist)
                if res not in [SetValueReturnCode.Ok,
                               SetValueReturnCode.DuplicateValue]:
                    if __debug__:
                        msg = 'SetStyle\n'
                        for k, v in arglist.items():
                            msg += '  {}: {}\n'.format(k, v)
                        raise TecplotSystemError(str(res) + '\n' + msg)
                    raise TecplotSystemError(res)
            except TecplotLogicError as e:
                if __debug__:
                    msg = 'SetStyle\n'
                    for k, v in arglist.items():
                        msg += '  {}: {}\n'.format(k, v)
                    raise TecplotLogicError(str(e) + '\n' + msg)
                else:
                    raise

        finally:
            for a in allocd:
                a.dealloc()


def get_style(return_type, *args, **kwargs):
    if __debug__:
        assert len(args) < 7

        if log.getEffectiveLevel() < logging.INFO:
            msg = 'GetStyle\n'
            for a in args:
                msg += '  {} {}\n'.format(type(a), a)
            for k, v in kwargs.items():
                msg += '  {} : {} {}\n'.format(k, type(v), v)
            log.debug(msg[:-1])

            _tecutil_connector._style_call_count['GET'][' '.join(args)] += 1

    if return_type in [IndexRange]:
        args = list(args)
        imin = get_style(Index, *(args + [sv.MIN]), **kwargs)
        imax = get_style(Index, *(args + [sv.MAX]), **kwargs)
        istep = get_style(int, *(args + [sv.SKIP]), **kwargs)
        return IndexRange(imin, imax, istep)
    elif return_type in [XYPosition]:
        args = list(args)
        x = get_style(float, *(args + [sv.X]), **kwargs)
        y = get_style(float, *(args + [sv.Y]), **kwargs)
        return XYPosition(x, y)
    elif return_type in [XYZPosition]:
        args = list(args)
        x = get_style(float, *(args + [sv.X]), **kwargs)
        y = get_style(float, *(args + [sv.Y]), **kwargs)
        z = get_style(float, *(args + [sv.Z]), **kwargs)
        return XYZPosition(x, y, z)

    with tecutil.ArgList() as arglist:

        allocd = []
        try:

            for i, p in enumerate(args):
                arglist[getattr(sv, 'P' + str(i + 1))] = p

            for k, v in kwargs.items():
                k = k.upper()
                if k == sv.UNIQUEID:
                    v = c_size_t(v)
                elif k in [sv.OBJECTSET]:
                    v = IndexSet(*v)
                    allocd.append(v)
                elif k in [sv.OFFSET1, sv.OFFSET2]:
                    v = v + 1
                arglist[k] = v

            if (return_type in [int, bool, Index, list, set] or
                    issubclass(return_type, Enum)):
                arglist[sv.IVALUE] = pointer(c_size_t())
            elif return_type in [str]:
                arglist[sv.IVALUE] = pointer(pointer(c_char()))
            elif return_type in [float]:
                arglist[sv.DVALUE] = pointer(c_double())
            else:
                raise TecplotTypeError('unknown return_type: {}'.format(return_type))

            if __debug__:
                if log.getEffectiveLevel() < logging.INFO:
                    msg = 'GetStyle\n'
                    for k, v in arglist.items():
                        msg += '  {}: {}\n'.format(k, v)
                    log.debug(msg[:-1])

            try:
                res = _tecutil.StyleGetLowLevelX(arglist)
                if res is not GetValueReturnCode.Ok:
                    raise TecplotSystemError(res)
            except TecplotLogicError as e:
                if __debug__:
                    msg = 'GetStyle\n'
                    for k, v in arglist.items():
                        msg += '  {}: {}\n'.format(k, v)
                    raise TecplotLogicError(str(e) + '\n' + msg)
                else:
                    raise

            if return_type in [str]:
                ivalue = ctypes.cast(arglist[sv.IVALUE], POINTER(c_char_p))
                result = ivalue.contents.value
                if result not in [None, '']:
                    result = result.decode('utf-8')
            elif issubclass(return_type, Enum):
                ival = arglist[sv.IVALUE]
                val = ctypes.cast(ival, POINTER(c_int64)).contents.value
                result = return_type(int(val))
            elif return_type in [Index]:
                ival = arglist[sv.IVALUE]
                val = ctypes.cast(ival, POINTER(c_int64)).contents.value
                result = return_type(int(val) - 1)
            elif return_type in [list, set]:
                ptr = ctypes.cast(arglist[sv.IVALUE], POINTER(IndexSet))
                iset = ptr.contents
                result = return_type(iset)
                iset.dealloc()
            elif return_type in [int, bool]:
                result = return_type(arglist[sv.IVALUE].contents.value)
            else:  # if return_type in [float]:
                result = return_type(arglist[sv.DVALUE].contents.value)

            if __debug__:
                if log.getEffectiveLevel() < logging.INFO:
                    log.debug('GetStyle result: {}'.format(result))

            return result

        finally:
            for a in allocd:
                a.dealloc()


@lock_attributes
class Style(object):
    def __init__(self, *svargs, **kwargs):
        self._uniqueid = kwargs.pop('uniqueid', None)
        self._offset1 = kwargs.pop('offset1', None)
        self._offset2 = kwargs.pop('offset2', None)
        self._multiset = kwargs.pop('multiset', False)
        if __debug__:
            assert not (self._offset2 and self._multiset)
        self._sv = list(flatten_args(*svargs))
        self._get_style_kwargs = {}
        self._set_style_kwargs = {}
        if self._uniqueid is not None:
            self._get_style_kwargs[sv.UNIQUEID] = self._uniqueid
            self._set_style_kwargs[sv.UNIQUEID] = self._uniqueid
        if self._offset1 is not None:
            self._get_style_kwargs[sv.OFFSET1] = self._offset1
            if self._multiset:
                self._set_style_kwargs[sv.OBJECTSET] = {self._offset1}
            else:
                self._set_style_kwargs[sv.OFFSET1] = self._offset1
            if self._offset2 is not None:
                self._get_style_kwargs[sv.OFFSET2] = self._offset2
                self._set_style_kwargs[sv.OFFSET2] = self._offset2

    @property
    def _style_attrs(self):
        if not hasattr(self, '_cached_style_attrs'):
            attrs = dict(uniqueid = self._uniqueid,
                         offset1 = self._offset1,
                         offset2 = self._offset2,
                         multiset = self._multiset)
            self._cached_style_attrs = {k:v for k,v in attrs.items()
                                        if v is not None}
        return self._cached_style_attrs

    def _get_style(self, rettype, *svargs, **kwargs):
        svargs = self._sv + list(svargs)
        kw = self._get_style_kwargs.copy()
        kw.update(**kwargs)
        return get_style(rettype, *svargs, **kw)

    def _set_style(self, value, *svargs, **kwargs):
        svargs = self._sv + list(svargs)
        kw = self._set_style_kwargs.copy()
        kw.update(**kwargs)
        set_style(value, *svargs, **kw)


class StyleConfig(Style):
    """Runtime Configuration Control Base Class."""
    def __init__(self, name=None, *svargs):
        if svargs:
            Style.__init__(self, *svargs)
        self._ns = name.split('.') if name else []

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            if not hasattr(self, '_keys'):
                self._keys = list(filter(lambda x: not x.startswith('_'), dir(self)))
            if name not in self._keys:
                msg = 'No configuration found: '
                raise TecplotAttributeError(msg + '.'.join(self._ns + [name]))
        super().__setattr__(name, value)

    @property
    def _opts(self):
        if not hasattr(self, '_attrs'):
            configs, props = [], []
            for key in filter(lambda x: not x.startswith('_'), dir(self)):
                value = getattr(self, key)
                if isinstance(value, StyleConfig):
                    configs.append((key, value))
                else:
                    props.append(key)
            self._attrs = (sorted(configs), sorted(props))
        return self._attrs

    def __str__(self):
        configs, props = self._opts
        lines = []
        for keyname in props:
            key = '.'.join(self._ns + [keyname])
            lines.append('{} = {}'.format(key, getattr(self, keyname)))
        for _, value in configs:
            lines.append(str(value))
        return '\n'.join(lines)


def style_property(value_type, sv):
    def getter(self, value_type=value_type, sv=sv):
        return self._get_style(value_type, sv)

    def setter(self, val, value_type=value_type, sv=sv):
        self._set_style(value_type(val), sv)

    return property(getter, setter)
