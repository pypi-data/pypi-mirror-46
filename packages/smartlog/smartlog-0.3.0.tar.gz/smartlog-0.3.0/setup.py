import os
from setuptools import setup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(THIS_DIR, 'README.md')) as f:
	long_description = f.read()

setup(
	name='smartlog',
	version='0.3.0',
	description='Tools to log exceptions and better interface with logging library',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/dnut/smartlog',
	author='Drew Nutter',
	author_email='drew@drewnutter.com',
	license='GPLv3',
	package_dir={'': 'src'},
	packages=['smartlog'],
	zip_safe=False,
)
