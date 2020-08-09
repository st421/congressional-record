from codecs import open
import sys
import os
from setuptools import find_packages, setup


INSTALL_REQUIRES = (
    'beautifulsoup4 >= 4.4.0',
    'click < 8.0',
    'html2ans >= 3.0.0',
    'jmespath',
    'lxml >= 3.3.5',
    'requests',
    'xmltodict',
    'python-dateutil'
)
NEEDS_DOCS = 'build_sphinx' in sys.argv
NEEDS_PYTEST = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
DOCS_REQUIRE = ('sphinx',)
TESTS_REQUIRE = (
    'pycodestyle',
    'pytest',
    'pytest-cov'
)
DEV_REQUIRE = (
    'autopep8',
    'pycodestyle',
    'pylint',
    'tox',
    'twine'
)
SETUP_REQUIRES = (('pytest-runner',) if NEEDS_PYTEST else ()) + (DOCS_REQUIRE if NEEDS_DOCS else () + DEV_REQUIRE)
EXTRAS_REQUIRE = {
    'dev': DOCS_REQUIRE + TESTS_REQUIRE,
    'tests': TESTS_REQUIRE
}
THIS_FILE_DIR = os.path.dirname(__file__)

LONG_DESCRIPTION = ''
# Get the long description from the README file
with open(os.path.join(THIS_FILE_DIR, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# The full version, including alpha/beta/rc tags
RELEASE = '0.0.1'
# The short X.Y version
VERSION = '.'.join(RELEASE.split('.')[:2])

PROJECT = 'congressionalrecord'
AUTHOR = ''
COPYRIGHT = '2020, {}'.format(AUTHOR)


setup(
    name=PROJECT,
    version=RELEASE,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7'
    ],
    description='Parse the U.S. Congressional Record from Govinfo.',
    long_description=LONG_DESCRIPTION,
    license='MIT',
    packages=find_packages('src', exclude=['docs', 'tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require=EXTRAS_REQUIRE,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', PROJECT),
            'version': ('setup.py', VERSION),
            'release': ('setup.py', RELEASE)
        }
    },
    py_modules=['congressionalrecord'],
    entry_points='''
        [console_scripts]
        cr=congressionalrecord.cli:cli
    '''
)
