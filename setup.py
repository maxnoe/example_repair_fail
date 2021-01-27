import os
import sys
import sysconfig
import subprocess as sp

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


SETUP_DIR = os.path.abspath(os.path.dirname(__file__))


class CMakeExtension(Extension):
    def __init__(self, name, source_dir=None, target=None, **kwargs):
        if source_dir is None:
            self.source_dir = SETUP_DIR
        else:
            self.source_dir = os.path.join(SETUP_DIR, source_dir)
        self.target = target
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[], **kwargs)


class build_ext_cmake(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        for d in (self.build_temp, extdir):
            os.makedirs(d, exist_ok=True)

        cfg = 'Debug' if self.debug else 'RelWithDebInfo'
        rpath = '@loader_path' if sys.platform == 'darwin' else '$ORIGIN'
        python_lib = os.path.join(
            sysconfig.get_config_var('LIBDIR'),
            sysconfig.get_config_var('INSTSONAME'),
        )
        cmake_call = [
            "cmake",
            ext.source_dir,
            '-DCMAKE_BUILD_TYPE=' + cfg,
            '-DPYTHON_EXECUTABLE=' + sys.executable,
            '-DPYTHON_LIBRARY=' + python_lib,
            '-DPYTHON_INCLUDE_DIR=' + sysconfig.get_path('include'),
            '-DCMAKE_INSTALL_RPATH={}'.format(rpath),
            '-DCMAKE_BUILD_WITH_INSTALL_RPATH:BOOL=ON',
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=OFF',
        ]
        sp.run(cmake_call, cwd=self.build_temp, check=True)
        build_call = [
            'cmake',
            '--build', '.',
            '--config', cfg,
        ]
        if ext.target is not None:
            build_call.extend(['--target', ext.target])

        build_call.extend(['--', '-j{}'.format(os.getenv('BUILD_CORES', 2))])
        sp.run(build_call, cwd=self.build_temp, check=True)


setup(
    name='example_repair_fail',
    version='0.1.0',
    ext_modules=[
        CMakeExtension('pyfoo', target='pyfoo'),
    ],
    cmdclass={
        'build_ext': build_ext_cmake,
    },
    zip_safe=False,
)

