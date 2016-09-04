from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='arlo',
    version='0.0.1',
    description='Python package for interacting with Netgear Arlo cameras via the apis that are consumed by their website.',
    long_description=readme,
    author='Jeffrey D. Walter',
    author_email='me@jeffreydwalter.com',
    url='https://github.com/jeffreydwalter/arlo',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
