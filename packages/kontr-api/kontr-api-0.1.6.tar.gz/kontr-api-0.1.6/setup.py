import re
from pathlib import Path

from setuptools import find_packages, setup

LONG_DESC = Path('README.md').read_text(encoding='utf-8')

VERSION = re.search(r'__version__ = \'(.*?)\'',
                    Path('kontr_api/__init__.py').read_text(encoding='utf-8')
                    ).group(1)

requirements = ['requests', 'pyjwt', 'PyYAML']

extra_requirements = {
    'dev': [
        'pytest',
        'coverage',
        'mock',
    ],
    'docs': ['sphinx']
}

setup(name='kontr-api',
      version=VERSION,
      description='Kontr Portal REST Api Client',
      author='Peter Stanko',
      author_email='stanko@mail.muni.cz',
      maintainer='Peter Stanko',
      url='https://gitlab.fi.muni.cz/grp-kontr2/kontr-api',
      packages=find_packages(exclude=("tests",)),
      long_description=LONG_DESC,
      long_description_content_type='text/markdown',
      include_package_data=True,
      install_requires=requirements,
      extras_require=extra_requirements,
      entry_points={},
      classifiers=[
          "Programming Language :: Python :: 3",
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          "Operating System :: OS Independent",
          "License :: OSI Approved :: Apache Software License",
          'Intended Audience :: Developers',
          'Topic :: Utilities',
      ],
      )
