#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import argparse
import contextlib
import os
import platform
import subprocess
import sys
import tempfile
import textwrap


SUPPORTED_PYTHON_VERSIONS = [(2,7), (3,4), (3,5), (3,6), (3,7)]


def write_coveragerc(fname):
    fmt = textwrap.dedent("""\
        [report]
        # Regexes for lines to exclude from consideration
        exclude_lines =
            pragma: no cover
        {pyver}
        {system}
            if 0:
            if False:
            if __name__ == .__main__.:

        omit =
            tecplot/tecutil/constant.py
            tecplot/tecutil/message_pb2.py
            tecplot/tecutil/sv.py
            tecplot/tecutil/tecutil.py
            tecplot/tecutil/tecutil_rpc.py
            tecplot/tecutil/tecutil_flatbuffers/*
    """)

    opts = {}

    version = sys.version_info[:2]
    assert version in SUPPORTED_PYTHON_VERSIONS

    pyver = ''
    def vinfo(op, v):
        s = '        if sys\.version_info {op} \({v}\n'
        return s.format(op=op, v=', '.join(str(x) for x in v))
    for v in sorted(set(x[0] for x in SUPPORTED_PYTHON_VERSIONS)):
        if v < version[0]:
            pyver += vinfo('<=?', [v])
        elif v == version[0]:
            pyver += vinfo('[<>]', [v])
            for vv in sorted(filter(lambda x: x[0]==v,
                                    SUPPORTED_PYTHON_VERSIONS)):
                if vv < version:
                    pyver += vinfo('<=?', vv)
                elif vv == version:
                    pyver += vinfo('[<>]', vv)
                else:
                    pyver += vinfo('>=?', vv)
        else:
            pyver += vinfo('>=?', [v])
    opts['pyver'] = pyver

    lin = '[Ll]inux'
    win = '[Ww]indows'
    mac = '[Dd]arwin'
    if platform.system() == 'Windows':
        target = win
        others = (lin,mac)
    elif platform.system() == 'Darwin':
        target = mac
        others = (win,lin)
    else: #if platform.system() == 'Linux':
        target = lin
        others = (win,mac)

    opts['system'] = """\
    if platform\.system.*(?!{0})

    def.*{1}.*(?!{0})
    def.*(?!{0}).*{1}
    def.*{2}.*(?!{0})
    def.*(?!{0}).*{2}
""".format(target,*others)

    with open(fname, 'w+t') as fout:
        fout.write(fmt.format(**opts))


def run(cmd, **env):
    #print(env)
    opts = {'env': os.environ.copy()}
    opts['env'].update(**env)
    if platform.system() != 'Windows':
        opts['shell'] = True
    proc = subprocess.Popen(cmd, **opts)
    return proc.wait()


@contextlib.contextmanager
def temporary_file(*args, **kwargs):
    kwargs['delete'] = False
    with tempfile.NamedTemporaryFile(*args, **kwargs) as ftmp:
        ftmp.close()
        try:
            yield ftmp.name
        finally:
            try:
                os.remove(ftmp.name)
            except (OSError, FileNotFoundError) as e:
                print(e)
                print('could not clean up temporary file: {}'.format(ftmp.name))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-coverage', action='store_true')
    parser.add_argument('--source', default='tecplot')
    parser.add_argument('test', nargs=argparse.REMAINDER,
        default=['test', '--random', '--failfast', 'buffer'])
    args = parser.parse_args()

    opts = dict(
        py = sys.executable,
        cov = 'coverage run',
        opts = '--module --branch',
        args = ' '.join(args.test[1:] if len(args.test) > 1 else []),
        tst = args.test[0],
        src = args.source)

    if args.no_coverage:
        cmds = [
            '{py} -m {tst} {args}',
            '{py} -O -m {tst} {args}',
        ]
        rc = 1
        for cmd in cmds:
            cmd = cmd.format(**opts)
            rc = run(cmd)
            if rc != 0:
                break
    else:
        cmds = ['{py} -m coverage erase {rc}',
                '{py} -m {cov} {rc} {opts} --source={src} {tst} {args}',
                '{py} -O -m {cov} {rc} --append {opts} --source={src} {tst} {args}',
                '{py} -O -m coverage report {rc} --show-missing']
        rc = 1
        with temporary_file(mode='w+t') as coveragerc:
            write_coveragerc(coveragerc)
            with temporary_file(mode='w+t') as coverage_results:
                opts['rc'] = '--rcfile="{}"'.format(coveragerc)
                for cmd in cmds:
                    cmd = cmd.format(**opts)
                    rc = run(cmd, COVERAGE_FILE=coverage_results)
                    if rc != 0:
                        break

    sys.exit(rc)


if __name__ == '__main__':
    main()
