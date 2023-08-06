#!/usr/bin/env python
import subprocess
import sys

try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand

    class PyTest(TestCommand):
        extra_kwargs = {'tests_require': ['pytest', 'mock']}

        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            import pytest
            sys.exit(pytest.main(self.test_args))

except ImportError:
    from distutils.core import setup, Command

    class PyTest(Command):
        extra_kwargs = {}
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            raise SystemExit(subprocess.call([sys.executable, 'runtests.py']))

try:
   import pypandoc
   readme = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError, RuntimeError):
   readme = ''

setup(name='allow',
      version='0.0.2',
      description="Personal Website Safe and Block List Management Script",
      long_description=readme,
      author='Timothy Crosley',
      author_email='timothy.crosley@gmail.com',
      url='https://github.com/timothycrosley/allow',
      license='MIT',
      requires=['hug'],
      install_requires=['hug>=2.5.0', 'tldextract'],
      entry_points={
        'console_scripts': [
            'allow = allow.run:allow.interface.cli',
        ]
      },
      packages=['allow'],
      keywords='Focus, Python, Python3, Firewall, Filter, Utility, Block, Allow',
      **PyTest.extra_kwargs)
