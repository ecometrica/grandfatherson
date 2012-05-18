#!/usr/bin/env python

from distutils.core import setup
from distutils.cmd import Command

import os
import re
import subprocess
import sys


_dir_ = os.path.dirname(__file__)


class test(Command):
    description = "run tests"
    user_options = [
        ('tests=', 't', 'test names, separated by commas'),
    ]

    def initialize_options(self):
        self.tests = None

    def finalize_options(self):
        if self.tests is not None:
            self.tests = re.split('[, ]+', self.tests)

    def run(self):
        """Run test/tests.py and quit with exit status"""
        progname = os.path.join(_dir_, 'run-tests.py')
        cmd = [sys.executable, progname]
        if self.verbose == 0:
            cmd.append('--quiet')
        elif self.verbose >= 2:
            cmd.append('--verbose')
        if self.tests:
            cmd.extend(self.tests)
        retcode = subprocess.call(cmd)
        if retcode != 0:
            sys.exit(retcode)


def long_description():
    sys.path.insert(0, _dir_)
    import grandfatherson
    return grandfatherson.__doc__


setup(name='GrandFatherSon',
      version='1.0',
      description='Grandfather-father-son backup rotation calculator',
      long_description=long_description(),
      author='Ecometrica',
      author_email='info@ecometrica.com',
      url='http://github.com/ecometrica/grandfatherson/',
      packages=['grandfatherson'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries',
          'Topic :: System :: Archiving',
      ],
      license='BSD License',
      cmdclass={'test': test},
)
