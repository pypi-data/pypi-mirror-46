import os
from setuptools import setup, find_packages

from script_pattern import __version__


base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()

setup(
    name='django-script-pattern',
    version=__version__,
    description='Django script pattern app',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='Maxim Shaitanov',
    author_email='maximshaitanov@gmail.com',
    url='https://gitlab.com/kastielspb/django-script-pattern',
    packages=find_packages(exclude=['example', 'tests']),
    include_package_data=True,
    license='MIT',
    install_requires=[
        'django',
        'django-jinja',
        'django-admin-sortable2'
    ],
    classifiers=[
        'Environment :: Web Environment',
        "Operating System :: OS Independent",
        "Framework :: Django",
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
