from distutils.core import setup

from setuptools import find_packages

from viewsets import __version__


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='django-view-sets',
    version=__version__,
    description='Yet another app for making CRUD.',
    long_description=readme(),
    keywords=['django', 'views', 'viewset', 'crud'],
    author='Grigory Mishchenko',
    author_email='grishkokot@gmail.com',
    url='https://github.com/kindlycat/django-view-sets/',
    packages=find_packages(exclude=('manage', 'tests', 'tests.*')),
    include_package_data=True,
    install_requires=['Django>=2.0', 'django-filter>=2.1.0'],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'License :: OSI Approved :: BSD License',
    ],
)
