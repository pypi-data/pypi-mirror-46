# python
# -*- coding: utf-8 -*-

"""Setup module for helpdev.

Since:
    2019/04/20

Authors:
    - Daniel Cosmo Pizetta <daniel.pizetta@usp.br>
"""

import codecs
import os
import re

from setuptools import find_packages, setup


def find_version(*file_paths):
    """Find version in a Python file, searching for the __version__."""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def read(*parts):
    """Read files."""
    # intentionally *not* adding an encoding option to open, See:
    # https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r').read()


_long_description = read('README.rst')
_version = find_version("helpdev", "__init__.py")

_classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Customer Service',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Documentation',
    'Topic :: Software Development :: Bug Tracking',
    'Topic :: Software Development :: Documentation',
    'Topic :: Software Development :: Debuggers',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Testing',
    'Topic :: Terminals']

_requires = ['importlib_metadata', 'psutil>=5.6']

setup(name='helpdev',
      version=_version,
      description='HelpDev - Extracts information about the Python environment easily.',
      long_description=_long_description,
      license_file='LICENSE.rst',
      author='Daniel Cosmo Pizetta',
      author_email='daniel.pizetta@usp.br',
      maintainer='Daniel Cosmo Pizetta',
      maintainer_email='daniel.pizetta@usp.br',
      packages=find_packages(),
      classifiers=_classifiers,
      install_requires=_requires,
      entry_points={"console_scripts": ["helpdev=helpdev.__main__:main"]},
      url='https://gitlab.com/dpizetta/helpdev',
      project_urls={
          "Issues": "https://gitlab.com/dpizetta/helpdev/issues",
          "Docs": "https://helpdev.readthedocs.io/en/stable/index.html",
      }
      )
