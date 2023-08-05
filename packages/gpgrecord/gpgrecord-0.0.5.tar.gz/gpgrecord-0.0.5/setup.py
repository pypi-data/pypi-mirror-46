# Copyright (c) 2018 WeFindX Foundation, CLG.
# All Rights Reserved.

from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='gpgrecord',
    version='0.0.5',
    description='Encrypt/Decrypt interface for GPG record compatiable with JSON via base64.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wefindx/gpgrecord',
    author='Mindey',
    author_email='mindey@qq.com',
    license='MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'python-gnupg>=0.4.4',
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)
