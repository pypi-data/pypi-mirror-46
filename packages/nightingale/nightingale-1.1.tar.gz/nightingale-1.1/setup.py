from setuptools import setup, find_packages

setup(
      name='nightingale',
      version='1.1',
      description='Python library for simplifying statistical analysis and making it more consistent',
      url='https://github.com/idin/nightingale',
      author='Idin',
      author_email='py@idin.ca',
      license='MIT',
      packages=find_packages(exclude=("jupyter_tests")),
      install_requires=['statsmodels'],
      zip_safe=False
)