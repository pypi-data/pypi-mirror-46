from setuptools import setup

with open('README.txt') as file:
    long_description = file.read()

setup(name='ibmdb2',
      version='0.2',
      description='IBM-DB2 Wrapper Class',
      long_description=long_description,
      url='https://github.com/ipal0/ibmdb2',
      author='Pal',
      author_email='ipal00@outlook.com',
      license='GPL',
      python_requires='>=3',
      packages=['ibmdb2'])
