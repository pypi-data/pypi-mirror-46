# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from django_cloud_essentials import __version__


setup(
    name="django-cloud-essentials",
    version=__version__,
    description='An opinionated django setup for Divio Cloud',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://www.divio.com',
    packages=find_packages(),
    install_requires=(
        'Django',
        'django-getenv',
    ),
    include_package_data=True,
    zip_safe=False,
)
