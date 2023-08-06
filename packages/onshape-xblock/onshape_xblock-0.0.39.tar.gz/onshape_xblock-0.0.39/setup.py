"""Setup for onshape_xblock XBlock."""

import os

from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='onshape_xblock',
    version='0.0.39',
    description='The Onshape Xblock used to grade Onshape elements according to a number of criteria.',
    license='MIT',
    packages=[
        'onshape_xblock',
    ],
    install_requires=[
        'utils',
        'xblock',
        'xblock-utils',
        'pathlib',
        'pint',
        'jsonpickle',
        'onshape-client',
        'django',
        'jinja2',
        'ruamel.yaml',
        'uncertainties',
        'importlib_resources'
    ],
    entry_points={
        'xblock.v1': [
            'onshape_xblock = onshape_xblock:OnshapeXBlock'
        ]
    },
    package_data=package_data("onshape_xblock", ["static", "public", "templates", "checks"]),
)
