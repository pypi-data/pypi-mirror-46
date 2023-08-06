'''
@Author: LogicJake
@Date: 2019-05-24 19:48:17
@LastEditTime: 2019-05-24 20:45:50
'''
import os
import sys

import pkg_resources
import setuptools

try:
    if int(pkg_resources.get_distribution("pip").version.split('.')[0]) < 6:
        print('pip older than 6.0 not supported, please upgrade pip with:\n\n'
              '    pip install -U pip')
        sys.exit(-1)
except pkg_resources.DistributionNotFound:
    pass

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = sys.version_info[:2]
if version < (3, 5):
    print('labssh requires Python version 3.5 or later' +
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)

install_requires = ['requests', 'PyYAML']
VERSION = '1.1.0'

setuptools.setup(
    name='print2message',
    version=VERSION,
    description="Forward 'print' content",
    long_description_content_type='text/markdown',
    author='LogicJake',
    author_email='chenyangshi1996@gamil.com',
    url='https://github.com/LogicJake/print2message',
    long_description=long_description,
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    zip_safe=False,
    license='MIT',
)
