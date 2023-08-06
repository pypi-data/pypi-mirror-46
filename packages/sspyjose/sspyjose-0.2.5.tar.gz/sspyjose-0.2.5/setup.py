#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python package setup tooling."""

from codecs import open
from os import path
from subprocess import check_call

from setuptools import setup, find_packages
from setuptools.command.develop import develop


__version__ = '0.2.5'

here = path.abspath(path.dirname(__file__))


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        """
        Install pre-commit git hooks for given project.
        """
        develop.run(self)
        # Install the pre-commit and pre-push hooks using `pre-commit`.
        check_call('pre-commit install'.split())
        check_call('pre-commit install --hook-type pre-push'.split())


def long_description():
    """Get the long description from the README file."""
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()


def install_requires(label=None, include_repo_links=True):
    """Get the dependencies and installs."""
    req_file = ('requirements-{}.txt'.format(label) if label
                else 'requirements.txt')
    with open(path.join(here, req_file), encoding='utf-8') as f:
        all_reqs = f.read().split('\n')
    packages = [x.strip() for x in all_reqs if 'git+' not in x]
    repo_links = [x.strip().replace('git+', '')
                  for x in all_reqs if x.startswith('git+')]
    if include_repo_links:
        return packages + repo_links
    else:
        return packages


setup(
    name='sspyjose',
    version=__version__,
    description=('An (interim) JOSE library, featuring support for'
                 ' Ed25519, X25519, ChaCha20/Poly1305 and AES256-GCM'
                 ' as required for PyKauriID'),
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/kauriid/sspyjose.git',
    license='Apache License 2.0',
    # See here for `classifiers`:
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=('singlesource blockchain data kauri kauriid identity'
              ' self-sovereign jose jwt jws jwe jwk'),
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Guy K. Kloss',
    install_requires=install_requires(),
    dependency_links=install_requires(include_repo_links=True),
    author_email='guy@mysinglesource.io',

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': install_requires('dev'),
        'test': install_requires('test')
    }
)
