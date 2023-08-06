"""
Setup file for ci.
"""

import io
import os
import re

from setuptools import setup


def get_metadata():
    """
    Return metadata for ci.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    init_path = os.path.join(here, 'ci.py')
    readme_path = os.path.join(here, 'README.md')

    with io.open(init_path, encoding='utf-8') as f:
        about_text = f.read()

    metadata = {
        key: re.search(r'__' + key + r"__ = '(.*?)'", about_text).group(1)
        for key in ('title', 'version', 'url', 'author', 'author_email', 'license', 'description')
    }
    metadata['name'] = metadata.pop('title')

    with io.open(readme_path, encoding='utf-8') as f:
        metadata['long_description'] = f.read()
        metadata['long_description_content_type'] = 'text/markdown'

    return metadata


metadata = get_metadata()

# Primary requirements
install_requires = [
    'click'
]
entry_points = {
    'console_scripts': [
        'ci=ci:cli'
    ]
}

# Development requirements
lint_requires = [
    'flake8 >=3.7.0',
    'flake8-comprehensions',
    'flake8-docstrings',
    'flake8-isort',
    'flake8-mutable',
    'flake8-pep3101',
    'flake8-quotes',
    'pep8-naming'
]
test_requires = [
    'pytest >=3.6.0',
    'pytest-cov',
    'mock'
]

setup(
    # Options
    install_requires=install_requires,
    extras_require={
        'dev.lint': lint_requires,
        'dev.test': test_requires
    },
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    py_modules=['ci'],
    entry_points=entry_points,

    # Metadata
    download_url='{url}/archive/{version}.tar.gz'.format(**metadata),
    project_urls={
        'Issue Tracker': '{url}/issues'.format(**metadata)
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    **metadata
)
