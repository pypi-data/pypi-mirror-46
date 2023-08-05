from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rawimage',
    version='0.0.2',
    description='Read and write RAW images (or data arrays) without a headache.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/ashkarin/rawimage',
    author='Andrei Shkarin',
    author_email='andrei.shkarin@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='ndarray data development reader writer raw-image image raw',
    packages=find_packages(exclude=['static']),
    install_requires=['numpy'],
    project_urls={
        'Bug Reports': 'https://github.com/ashkarin/rawimage/issues',
        'Source': 'https://github.com/ashkarin/rawimage'
    }
)
