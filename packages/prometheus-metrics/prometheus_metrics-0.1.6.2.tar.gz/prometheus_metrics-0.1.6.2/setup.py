import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='prometheus_metrics',
    version='0.1.6.2',
    url='https://github.com/dr1s/prometheus_metrics',
    author='Daniel Schmitz',
    license='MIT',
    description='Manage prometheus metrics',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['emby_exporter=emby_exporter:main']},
)
