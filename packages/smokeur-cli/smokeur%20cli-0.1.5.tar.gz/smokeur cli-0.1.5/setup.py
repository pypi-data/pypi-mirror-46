import os

import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name='smokeur cli',
    version='0.1.5',
    license='BSD',
    description='Smokeur client for CLI.',
    long_description=read('README.rst'),
    author='c0x6a',
    author_email='cj@carlosjoel.net',
    url='',
    packages=setuptools.find_packages(),
    scripts=['smokeur'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['requests', 'pyperclip']
)
