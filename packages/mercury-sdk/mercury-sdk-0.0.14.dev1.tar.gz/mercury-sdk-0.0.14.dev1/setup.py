# Copyright 2015 Jared Rodriguez (jared.rodriguez@rackspace.com)
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from setuptools import setup, find_packages

def get_version():
    with open('VERSION') as fp:
        return fp.read().strip()


setup(
    name='mercury-sdk',
    version=get_version(),
    packages=find_packages(exclude=['tests']),
    url='http://www.mercurysoft.io',
    license='Apache-2.0',
    author='Jared Rodriguez',
    author_email='jared.rodriguez@rackspace.com',
    description='Mercury HTTP client libraries, cli, and utilities',
    install_requires=[
        'requests',
        'PyYaml',
        'cmd2',
        'python-dateutil',
        'colorama'
    ],
    entry_points={
       'console_scripts': [
           'mcli=mercury_sdk.mcli.main:main'
       ]
    }
)
