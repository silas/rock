import os
import sys

from distutils.core import setup
from rock import __version__ as version

long_description = """
rock is a command line tool that simplifies building, testing, and running
applications in multiple languages and versions on the same system.

See http://www.rockstack.org for more information.
"""

install_requires = ['PyYAML']

if sys.version_info < (2, 7):
    install_requires += ['argparse']

if os.environ.get('CI') == 'true':
    install_requires += ['coverage', 'nose', 'pep8']
    if sys.version_info < (2, 7):
        install_requires += ['unittest2']

setup(
    name='rock',
    version=version,
    description='Rock Better Runtimes',
    long_description=long_description.strip(),
    author='Silas Sewell',
    author_email='silas@sewell.org',
    license='MIT',
    url='http://www.rockstack.org',
    packages=['rock'],
    package_data={'rock': ['data/*/*']},
    scripts=['scripts/rock'],
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
)
