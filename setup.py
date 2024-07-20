# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

gh_repo = 'https://github.com/weaming/thunder-subtitle-2024'

setup(
    name='thunder-subtitle',  # Required
    version='2024.7.20.1',  # Required
    description='下载迅雷看看字幕',  # Required
    url=gh_repo,  # Optional
    author='weaming',  # Optional
    author_email='garden.yuen@gmail.com',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    keywords='',  # Optional
    install_requires=[
        'drawtable @ git+https://github.com/weaming/drawtable.git',
    ],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'thunder-subtitle=thunder_subtitle_2024.__main__:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': gh_repo,
        'Source': gh_repo,
    },
)
