#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import setuptools

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'GitPython>=2.1.11']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setuptools.setup(
    author="Martin Skarzynski",
    author_email='marskar@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Extract code, markdown, and yaml files from R markdown.",
    entry_points={
        'console_scripts': [
            'camp=cli.camp_cli:camp_cli',
            'acmp=cli.acmp_cli:acmp_cli',
            'cam=cli.cam_cli:cam_cli',
            'acm=cli.acm_cli:acm_cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='gitone',
    name='gitone',
    package_dir={"": "src"},
    packages=setuptools.find_packages('src'),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marskar/gitone',
    version='0.0.15',
    zip_safe=False,
)
