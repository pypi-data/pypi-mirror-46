#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-ucamlookup',
    description='A Django module for the University of Cambridge Lookup service',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.developers.cam.ac.uk/uis/devops/django/ucamlookup',
    version='3.0.3',
    license='MIT',
    author='DevOps Division, University Information Services, University of Cambridge',
    author_email='devops@uis.cam.ac.uk',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django>=1.11'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
