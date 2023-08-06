# -*- coding: utf-8 -*-
from setuptools import setup
#from distutils.core import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
  name='jassa',
  packages = ['jassa'],
  version = '0.1.3',
  description='Just A Simple Sentiment Analysis Tool for Chinese Text',
  author = 'Hsin-Min Lu',
  author_email = 'luim@ntu.edu.tw',
  include_package_data = True,
  long_description=readme(),
  long_description_content_type = "/text/x-rst",
  classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
  keywords = ['sentiment_analysis Chinese'],
  install_requires=['pandas', 'jieba'],
  zip_safe=False,
  package_data={'':['data/*']},
  test_suite='nose.collector',
  tests_require=['nose'],
  #package_data={  # Optional
  #      'testdata': ['data/testdata.csv'],
  #      'model': ['model/*'],
  #},
  #url = 'https://github.com/yulun0528/namesex',
  #download_url = 'https://github.com/yulun0528/namesex/archive/2.5.tar.gz'
)
