import sys

from setuptools import setup, find_packages  # pylint: disable=no-name-in-module,import-error

install_requires = []

extras_require = {
  ":python_version<'3.4'": ['enum34'],
}

def dependencies(file):
    with open(file) as f:
        return f.read().splitlines()


setup(
    name='frkl.log_symbols',
    packages=find_packages(exclude=('tests', 'examples')),
    version='0.0.14',
    license='MIT',
    description='Colored symbols for various log levels for Python',
    long_description='Minor fork of: https://github.com/manrajgrover/py-log-symbols , until upstream versioning is fixed. Colored symbols for various log levels for Python. Find the documentation here: https://github.com/manrajgrover/py-log-symbols.',
    author='Markus Binsteiner',
    author_email='markus@frkl.io',
    url='https://github.com/frkl-downstream/py-log-symbols',
    keywords=[
        'log symbols',
        'symbols',
        'log'
    ],
    install_requires=dependencies('requirements.txt') + install_requires,
    extras_require=extras_require,
    tests_require=dependencies('requirements-dev.txt'),
    include_package_data=True
)
