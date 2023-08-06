# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='vgstash',
    version='0.3-beta5',
    description='a video game collection management module, backed by SQLite',
    long_description=readme,
    long_description_content_type="text/markdown; variant=CommonMark",
    author='zlg',
    license='AGPL-3.0-only',
    author_email='zlg+vgstash@zlg.space',
    url='https://git.zlg.space/vgstash',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=['vgstash_cli'],
    entry_points={
        'console_scripts': [
            'vgstash=vgstash_cli:cli',
            'vgstash_tk=vgstash_tk:main'
        ],
    },
    install_requires=[
        'Click>=6.0', # for CLI
        'PyYAML', # import/export YAML files
    ],
    classifiers=(
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
    ),
    project_urls={
        'Source': 'https://git.zlg.space/vgstash',
    }
)

