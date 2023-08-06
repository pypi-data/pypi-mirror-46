import os

import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name='smokeur cli',
    version='0.1.7',
    license='BSD',
    description='Smokeur client for CLI.',
    long_description=read('README.rst'),
    author='c0x6a',
    author_email='cj@carlosjoel.net',
    url='https://gitlab.com/c0x6a/smokeur-cli',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
    install_requires=['requests', 'pyperclip'],
    entry_points={
        'console_scripts': [
            'smokeur=smokeur:upload_file',
        ],
    },
)
