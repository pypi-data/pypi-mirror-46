
from setuptools import setup, find_packages

setup(
    name='jbrela-jakubBrela',
    version='0.4',
    packages=find_packages(exclude=['*']),
    license='MIT',
    description='An example python package',
    long_description=open('README.txt').read(),
    install_requires=['numpy'],
    url='https://pypi.org/manage/projects/',
    author='Jakub Brela'
)
