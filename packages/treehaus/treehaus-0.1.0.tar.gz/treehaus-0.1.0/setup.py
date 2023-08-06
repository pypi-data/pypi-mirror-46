"""setuptools based setup module for treehaus.
"""

from setuptools import setup, find_packages

setup(
    name='treehaus',

    version='0.1.0',

    description='Python3 persistent balanced trees',
    long_description="Python3 library for reading and writing persistent balanced trees",

    url='https://gitlab.com/treehaus/treehaus',

    author='TreeHaus Developers',
    author_email='',
    python_requires='>=3.5',

    license='OSI Approved :: Apache Software License',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='data storage btree',

    packages=find_packages(exclude=[]),

    install_requires=[],

    extras_require={
    },

    package_data={
    },

    entry_points={
    },
)
