"""
Setup Module to setup Python Handlers for LSST query templating
"""
import setuptools

setuptools.setup(
    name='jupyterlab_lsstquery',
    version='1.0.0-alpha6',
    packages=setuptools.find_packages(),
    install_requires=[
        'notebook',
    ],
    package_data={'jupyterlab_lsstquery': ['*']},
)
