
from setuptools import setup, find_packages

setup(
    name='python-package-example-Johnny-dpp',
    version='0.2',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='An example python package',
    long_description=open('README.txt').read(),
    install_requires=['numpy'],
    url='https://github.com/Johnny205/simplePythonLibrary',
    author='Mariusz Grabarczyk',
    author_email='grabmar97@gmaiil.com'
)
