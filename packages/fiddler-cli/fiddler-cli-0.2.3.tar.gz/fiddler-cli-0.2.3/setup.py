import re
import setuptools

with open('Readme.md', 'r') as fh:
    long_description = fh.read()


def find_version():
    for line in open('fiddler/cli.py'):
        for m in re.finditer(r"^__version__ = '(.*)'", line):
            return m[1]
    raise ValueError('Could not find __version__ in cli.py')


setuptools.setup(
    name='fiddler-cli',
    version=find_version(),
    author='Fiddler Labs',
    author_email='dev@fiddler.ai',
    description='CLI and tools for interacting with Fiddler Service',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://fiddler.ai',
    packages=setuptools.find_packages(),
    install_requires=[
        'boto3',
        'pandas>=0.2',
        'pyyaml',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'fiddler-cli = fiddler.cli:main',
            'fiddler = fiddler.cli:main',
            'fidl = fiddler.cli:main',
        ],
    },
)
