from setuptools import setup, find_packages

setup(
    name='TenHelloWorlds',
    version='0.5',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Learing to create python packages',
    long_description=open('README.md').read(),
    install_requires=[''],
    url='https://github.com/BlonskiP/TenHelloWorlds',
    author='Piotr Blonski',
    author_email='piotrblonski96@gmail.com'
)