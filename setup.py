#!/usr/bin/python

from setuptools import setup, find_packages

__version__ = '0.9'
__author__="Louis Dunne"
__author_email="louisadunne+ldapfs@gmail.com"
__url__ = 'http://pypi.python.org/pypi/bctree/'
__description__ = 'Basic Tree Implementation'
__long_description__ = __description__

__scripts__ = []


def run():
    setup(
        name='bctree',
        version=__version__,
        description=__description__,
        long_description=__long_description__,
        license='Apache 2.0',
        author='Louis A. Dunne',
        author_email='louisadunne@gmail.com',
        packages=find_packages(),
        zip_safe=False,
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: Apache Software License',
            'Intended Audience :: Developers',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
        ],
        scripts=__scripts__,
        url=__url__
    )

if __name__ == '__main__':
    run()
