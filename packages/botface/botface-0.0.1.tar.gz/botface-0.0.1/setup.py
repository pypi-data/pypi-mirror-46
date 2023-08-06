from setuptools import find_packages, setup

NAME = 'botface'
DESCRIPTION = 'Inspora Chat Engine'
URL = 'https://github.com/inspora/botface'
EMAIL = 'daniel@inspora.com'
AUTHOR = 'Daniel Birnstiel'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = '0.0.1'
README = ''

REQUIREMENTS = [
]

TEST_REQUIREMENTS = [
    'mock',
    'pytest',
    'pytest-cov',
    'freezegun'
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/plain',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=('tests', 'tests.*', 'example', 'example.*')
    ),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    include_package_data=True,
    license='',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)

