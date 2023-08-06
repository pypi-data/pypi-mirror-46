import os
import io
import re
from setuptools import find_packages, setup


def long_description():
    with io.open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme


setup(name='algorithms3',
      version='0.1.9',
      description='Data Structures and Algorithms using Python',
      long_description=long_description(),
      long_description_content_type="text/markdown",
      url='https://github.com/gulshalla/algorithms',
      author='Omar Shalla',
      author_email="omarhassangul@gmail.com",
      license='MIT',
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'
          ],
      zip_safe=False)