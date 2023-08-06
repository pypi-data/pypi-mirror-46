#!/usr/bin/env python

from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

setup(name='parmap',
      version='1.5.2',
      description=('map and starmap implementations passing additional '
                   'arguments and parallelizing if possible'),
      long_description=long_description,
      long_description_content_type = "text/x-rst",
      author='Sergio Oller',
      license='APACHE-2.0',
      author_email='sergioller@gmail.com',
      url='https://github.com/zeehio/parmap',
      packages=['parmap'],
      extras_require = {
          'progress_bar':  ["tqdm>=4.8.4"],
      },
      test_suite = "test_parmap",
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
      ],
)
