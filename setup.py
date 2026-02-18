#!/usr/bin/env python

from setuptools import setup, find_packages
import sys
import os
import fastentrypoints

# Enforce Python 3.12+
if sys.version_info < (3, 12):
    print(
        f"thefuck requires Python 3.12 or later "
        f"({sys.version_info.major}.{sys.version_info.minor} detected)."
    )
    sys.exit(-1)

if os.environ.get('CONVERT_README'):
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
else:
    long_description = ''

VERSION = '3.32'

install_requires = ['psutil', 'colorama', 'six']

extras_require = {
    ':python_version>"2.7"': ['decorator', 'pyte'],
    ":sys_platform=='win32'": ['win_unicode_console']
}

if sys.platform == "win32":
    scripts = ['scripts\\fuck.bat', 'scripts\\fuck.ps1']
    entry_points = {
        'console_scripts': [
            'thefuck = thefuck.entrypoints.main:main',
            'thefuck_firstuse = thefuck.entrypoints.not_configured:main'
        ]
    }
else:
    scripts = []
    entry_points = {
        'console_scripts': [
            'thefuck = thefuck.entrypoints.main:main',
            'fuck = thefuck.entrypoints.not_configured:main'
        ]
    }

setup(
    name='thefuck',
    version=VERSION,
    description="Magnificent app which corrects your previous console command",
    long_description=long_description,
    author='Vladimir Iakovlev',
    author_email='nvbn.rm@gmail.com',
    url='https://github.com/nvbn/thefuck',
    license='MIT',
    packages=find_packages(
        exclude=['ez_setup', 'examples', 'tests', 'tests.*', 'release']
    ),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.12',
    install_requires=install_requires,
    extras_require=extras_require,
    scripts=scripts,
    entry_points=entry_points
)
