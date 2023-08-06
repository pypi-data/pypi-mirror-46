from setuptools import find_packages
from setuptools import setup
import os

version = '1.0.0'

tests_require = [
]

extras_require = {
    'tests': tests_require,
}


setup(
    name='sentry-regressions',
    version=version,
    description='Sentry Plugin to better control regression handling',
    long_description=open('README.rst').read() + '\n' + open(
        os.path.join('docs', 'HISTORY.txt')).read(),

    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='Sentry Regressions Plugin',
    author='4teamwork AG',
    author_email='mailto:info@4teamwork.ch',
    url='https://github.com/4teamwork/sentry-regressions',
    license='GPL2',

    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
    ],

    tests_require=tests_require,
    extras_require=extras_require,

    entry_points={
        'sentry.plugins': [
            'sentry_regressions = sentry_regressions.plugin:RegressionPlugin'
        ],
        'sentry.apps': [
            'sentry_regressions = sentry_regressions'
        ],
    },
)
