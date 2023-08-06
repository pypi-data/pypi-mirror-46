from setuptools import setup

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='noolite_serial',
    version='0.1.1',
    packages=['noolite_serial'],
    url='',
    license='BSD',
    author='andrewgermanovich',
    author_email='andvikt@gmail.com',
    description='Noolite communication',
    install_requires=requirements
)
