import setuptools
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='configuration_layer',
    version='1.0.16',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    python_requires='~=3.6',
    url='https://github.com/antoniodimariano/client-side-service-discovery-confifguration-lab.git',
    license='MIT',
    author='Antonio Di Mariano',
    author_email='antonio.dimariano@gmail.com',
    description='client-side service discovery component for microservices.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['avro-python3', 'confluent-kafka', 'kafka',
                      'requests',
                      'microservices_messaging_layer',
                      'fastavro'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
)