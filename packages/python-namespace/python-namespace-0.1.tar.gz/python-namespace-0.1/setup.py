#!/usr/bin/env python
NAME = 'python-namespace'
AUTHOR = 'Tobias Gehring'
AUTHOR_EMAIL = 'tobias.gehring@fysik.dtu.dk'
LICENSE = 'LGPLv3'
URL = 'https://github.com/tobiasgehring/python-namespace'
DOWNLOAD_URL = 'https://github.com/tobiasgehring/python-namespace/archive/v0.1.tar.gz'
DESCRIPTION = 'Namespaces for class properties and methods'
LONG_DESCRIPTION = '''\
namespace provides namespaces for class properties and methods
'''
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Libraries',
    'Topic :: System :: Hardware',
    'Operating System :: Microsoft :: Windows'
]
PLATFORMS = ['all']
MAJOR               = 0
MINOR               = 1
ISRELEASED          = False
VERSION             = '%d.%d' % (MAJOR, MINOR)

if __name__=='__main__':

    from setuptools import setup

    setup(
        name = NAME,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        license = LICENSE,
        url = URL,
        download_url = DOWNLOAD_URL,
        version = VERSION,
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        classifiers = CLASSIFIERS,
        platforms = PLATFORMS,
        packages = ['namespace'])
