from setuptools import setup
import os

setup(
    name='pymutation',
    packages=['pymutation'],
    version='0.1.0',
    author='Kai Chang',
    author_email='kaijchang@gmail.com',
    url='https://github.com/kajchang/pymutation',

    license='MIT',
    long_description=open(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'README.md')).read(),
    long_description_content_type='text/markdown'
)
