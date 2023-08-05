from setuptools import setup, find_packages


from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kid-util',
    version='1.0.1',
    author='Halvor Holsten Strand',
    author_email='halvor.holsten.strand@gmail.com',
    url='https://github.com/Ondkloss/kid-util',
    description='Module for making and verifying KID numbers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='WTFPL',
    packages=find_packages(exclude=['test']),
)
