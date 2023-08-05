"""Setup script for object_detection."""

from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['Pillow>=1.0',
                     'Matplotlib>=2.1',
                     'Cython>=0.28.1',
                     'Protobuf',
                     'lxml',
                     'jupyter',
                     'matplotlib',
                     'tensorflow',
                     'contextlib2',
                     'wheel',
                     'twine']

setup(
    name='tensorflow_object_detection_api',
    maintainer='thebt995',
    maintainer_email='tkkg995@gmail.com',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    packages=[p for p in find_packages() if p.startswith('object_detection')],
    url='https://github.com/balazstothofficial/models',
    description='Tensorflow Object Detection Library Packaged',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
