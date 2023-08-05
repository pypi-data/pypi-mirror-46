from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
  name = 'laravalidation',
  packages=['laravalidation'],
  version = '0.4.1',
  description = 'Laravel like data validation library for python language',
  author = 'Walid Mashal',
  author_email = 'walidmashal4@gmail.com',
  url='https://github.com/kristopherchun/laravalidation.git',
  download_url = '',
  keywords = ['validation', 'python', 'laravel'],
  classifiers = [],
  long_description=long_description,
  long_description_content_type='text/markdown'
)
