from setuptools import setup, find_packages

setup(
    name='magic_square_dpp',
    version='1.2',
    packages=find_packages(exclude=['test*']),
    license='MIT',
    description='check if matrix is magic square',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
    url='https://gitlab.com/DanielSze/dpplab10',
    author='Daniel Szemik',
    author_email='szemikd226195@e-science.pl'
)
