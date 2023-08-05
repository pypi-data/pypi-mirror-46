""" setup file """
from setuptools import setup, find_packages

setup(
    name='notesviewer',
    version=open('notesviewer/_version').read(),
    description='notesviewer',
    packages=find_packages(),
    include_package_data=True,
    license='GPL',
    author='alekgr',
    author_email='alek.grigorian@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/Alekgr/notesviewer.git',
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        # operation system
        'Topic :: System :: Operating System Kernels :: Linux',
    ],

    entry_points={
        "console_scripts": [
            "notesviewer=notesviewer.nv:main",
        ]
    },

    install_requires=[
        'termcolor',
        'configparser',
    ]

)
