from distutils.core import setup
import setuptools


setup(
    name='webster',
    version='1.0',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pymongo',
        'more_itertools',
        'tldextract',
        'terminaltables'
    ],
    packages=[
        'webster',
        'webster.web'
    ],
    entry_points={
    },
   )
