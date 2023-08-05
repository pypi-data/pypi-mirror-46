from setuptools import setup, find_packages
import os
import sys
import subprocess

version = '0.1.2'

install_requires = [
    'pyocd',
    'pyserial>=3.4',
    'xmodem',
    'future',
    "pexpect",
    "click",
    "pyelftools",
    "pyyaml",
    'globster',
    'enum34'
]

version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcutk/_version.py')

if not os.path.exists(version_file):
    with open(version_file, 'w') as f:
        f.write("VERSION='%s'"%version)


setup(
    name="pymcutk",
    version=version,
    url='https://github.com/Hoohaha/pymcutk',
    description="MCU toolkit for mcu automated testing.",
    long_description=str(open('README.md', 'rb').read()),
    author="Haley Guo, Fly Yu",
    license="MIT License",
    author_email="hui.guo@nxp.com, chuzhi.yu@nxp.com",
    install_requires=install_requires,
    packages=["mcutk"],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mtk = mcutk.__main__:main',
        ]
    },
    setup_requires=[
        'setuptools',
        'setuptools-git',
        'wheel',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)