from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='nightingale',
	version='1.3',
	description='Python library for simplifying statistical analysis and making it more consistent',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/idin/nightingale',
	author='Idin',
	author_email='py@idin.ca',
	license='MIT',
	packages=find_packages(exclude=("jupyter_tests")),
	install_requires=['statsmodels', 'scipy', 'pandas'],
	python_requires='~=3.6',
	zip_safe=False
)