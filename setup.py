from setuptools import setup, find_packages

setup(
    name='congressionalrecord',
    version='0.9.1',
    description='Parse the U.S. Congressional Record from Govinfo.',
    url='https://github.com/unitedstates/congressional-record',
    author='Nick Judd',
    author_email='nick@nclarkjudd.com',
    license='BSD3',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4 >= 4.4.0',
        'lxml >= 3.3.5',
        'requests',
        'click < 8.0',
        'xmltodict',
        'jmespath'
        ],
    zip_safe=False
)
