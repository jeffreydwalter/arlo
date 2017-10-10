# coding=utf-8
"""Python Arlo setup script."""
from setuptools import setup

setup(
    name='pyarlo',
    packages=['pyarlo'],
    version='0.8.0',
    description='Python Arlo is a library written in Python 2.7/3x ' +
                'which exposes the Netgear Arlo cameras via the apis that are consumed by their website.',
    author='Jeffrey D. Walter',
    author_email='jeffreydwalter@gmail.com',
    url='https://github.com/jeffreydwalter/arlo',
    license=license,
    include_package_data=True,
    install_requires=['requests', 'sseclient', 'json'],
    keywords=[
        'arlo',
        'camera',
        'home automation',
        'netgear',
        'python',
        ],
    classifiers=[
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ' +
        'Apache License 2.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
