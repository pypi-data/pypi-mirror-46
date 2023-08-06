from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='api-tester-upload-test',
    version='1.1.3',
    description='Testing various  api  features',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='APIMatic SDK Generator',
    author_email='support@apimatic.io',
    url='https://apimatic.io',
    packages=find_packages(),
    install_requires=[
        'requests>=2.9.1, <3.0',
        'jsonpickle>=0.7.1, <1.0',
        'cachecontrol>=0.11.7, <1.0',
        'python-dateutil>=2.5.3, <3.0'
    ],
    tests_require=[
        'nose>=1.3.7'
    ],
    test_suite = 'nose.collector'
)