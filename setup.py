# coding=utf-8
"""Python Arlo setup script."""
from setuptools import setup

def readme():
    with open('README.md') as desc:
        return desc.read()

setup(
    name='arlo',
    py_modules=['arlo', 'request', 'eventstream'],
    version='1.2.64',
    description='Python Arlo is a library written in Python 2.7/3x ' +
                'which exposes the Netgear Arlo cameras via the apis that are consumed by their website.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Jeffrey D. Walter',
    author_email='jeffreydwalter@gmail.com',
    url='https://github.com/jeffreydwalter/arlo',
    license='Apache Software License',
    include_package_data=True,
    install_requires=['monotonic', 'requests', 'responses==0.10.15', 'urllib3==1.24', 'sseclient==0.0.22', 'PySocks', 'pickle-mixin', 'google-api-python-client', 'google-auth-oauthlib', 'curl-cffi==0.5.7'],
    keywords=[
        'arlo',
        'camera',
        'home automation',
        'netgear',
        'python',
        ],
    classifiers=[
	'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
	'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
