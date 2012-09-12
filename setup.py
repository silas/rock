from distutils.core import setup
from rock import __version__ as version

long_description = """
This is a command line tool that simplifies building, testing, and running
applications on the Rock Platform.

See http://www.rockplatform.org for more information.
"""

setup(
    name='rock',
    version=version,
    description='Rock Platform tool',
    long_description=long_description.strip(),
    author='Silas Sewell',
    author_email='silas@sewell.org',
    license='MIT',
    url='https://github.com/rockplatform/rock',
    packages=['rock'],
    package_data={'rock': [
        'data/*/*',
    ]},
    scripts=['scripts/rock'],
    install_requires=[
        'PyYAML',
        'argparse',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
