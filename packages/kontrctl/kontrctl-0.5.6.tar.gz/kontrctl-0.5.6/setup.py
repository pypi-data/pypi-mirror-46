import re
from pathlib import Path

from setuptools import find_packages, setup

long_description = Path('README.md').read_text(encoding='utf-8')

VERSION = re.search(r'__version__ = \'(.*?)\'',
                    Path('kontrctl/__init__.py').read_text(encoding='utf-8')
                    ).group(1)

requirements = ['click', 'kontr-api', 'tabulate', 'coloredlogs', 'pyyaml']

extras = {
    'dev': [
        'pytest',
        'coverage',
        'mock',
    ],
    'docs': ['sphinx']
}

classifiers = [
    "Programming Language :: Python :: 3",
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    "Operating System :: OS Independent",
    "License :: OSI Approved :: Apache Software License",
    'Intended Audience :: Developers',
    'Topic :: Utilities',
]

entry_points = {
    'console_scripts': [
        'kontrctl = kontrctl.cli:cli_main',
    ],
}

setup(name='kontrctl',
      version=VERSION,
      description='Kontr portal CLI',
      author='Peter Stanko',
      author_email='stanko@mail.muni.cz',
      url='https://gitlab.fi.muni.cz/grp-kontr2/kontrctl',
      packages=find_packages(exclude=("tests",)),
      long_description=long_description,
      long_description_content_type='text/markdown',
      include_package_data=True,
      install_requires=requirements,
      extras_require=extras,
      entry_points=entry_points,
      classifiers=classifiers,
      )
