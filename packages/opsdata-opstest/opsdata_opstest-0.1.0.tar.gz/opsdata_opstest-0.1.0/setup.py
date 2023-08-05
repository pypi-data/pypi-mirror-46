"""
The setup script for the dataset.
"""
import sys
from pathlib import Path

from setuptools import setup, find_packages

# make sure python 3 is running
if sys.version_info.major < 3:
    raise Exception(f"Obsplus datasets cannot be run on python 2")


def get_package_data_files():
    """ Create a list of datafiles """
    data_path = Path("opsdata_opstest") / "data"
    return [('', list(data_path.rglob()))]


# get requirements
requirements = open('requirements.txt')
test_requirements = open('tests/requirements.txt')

license_classifiers = {
    'BSD license': 'License :: OSI Approved :: BSD License',
}

setup(
    author="derrick chambers",
    author_email='djachambeador@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="a simple test of an obsplus dataset",
    entry_points={
        'obsplus.datasets': [
            'opstest=opsdata_opstest.core',
        ],
    },
    install_requires=requirements,
    license="BSD",
    include_package_data=True,
    name='opsdata_opstest',
    packages=find_packages(include=['ops_datasetopstest']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/d-chambers/opstest',
    version='0.1.0',
    zip_safe=False,
)
