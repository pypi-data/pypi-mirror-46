from setuptools import setup, find_packages
from os import path

with open("Readme.md", "r") as fh:
    long_description = fh.read()

# get the dependencies and installs
with open(path.realpath('requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='mfetcher',
    version='0.2',
    author='Aurel Megnigbeto',
    author_email='shiftsh@protonmail.ch',
    description='A simple cli tool to download mangas scan from the internet scan provider to your local file system',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sh1ftsh/mangas-scan-fetch',
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=dependency_links,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['mfetcher=mfetcher.command_line:main']
    },
    zip_safe=False)
