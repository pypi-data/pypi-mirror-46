# based on https://github.com/pypa/sampleproject
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mergesvvcf',

    version='1.0.1',

    description='Merge SV VCF calls. Fork of https://github.com/ljdursi/mergevcf by Jonathan Dursi (Jonathan.Dursi@oicr.on.ca)',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/papaemmelab/mergeSVvcf',

    # Author details
    author='Max Levine',
    author_email='levinem1@mskcc.org',

    # Choose your license
    license='GPL',

    classifiers=[
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',

        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    keywords='merge sv vcfs',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['pysam>=0.15.2','Cython>=0.29.7'],

    test_suite='tests',

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
#    package_data={
#        'sample': ['package_data.dat'],
#    },

    entry_points={
        'console_scripts': [
            'mergesvvcf=mergesvvcf:main',
        ],
    },
)
