#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'girder>=3.0.0a1'
]

setup(
    author="Zach Mullen",
    author_email='zach.mullen@kitware.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    description='Renders hyperlinks from metadata values',
    install_requires=requirements,
    license='Apache Software License 2.0',
    long_description=readme,
    include_package_data=True,
    keywords='girder-plugin, girder_metadata_links',
    name='girder-metadata-links',
    packages=find_packages(exclude=['test', 'test.*']),
    url='https://github.com/girder/girder_metadata_links',
    version='0.2.0',
    zip_safe=False,
    entry_points={
        'girder.plugin': [
            'girder_metadata_links = girder_metadata_links:GirderPlugin'
        ]
    }
)
