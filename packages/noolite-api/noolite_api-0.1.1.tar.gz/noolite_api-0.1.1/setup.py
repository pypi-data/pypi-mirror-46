from setuptools import setup

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='noolite_api',
    version='0.1.1',
    packages=['noolite_api'],
    url='https://github.com/andvikt/noolite_serial',
    license='BSD',
    author='andrewgermanovich',
    author_email='andvikt@gmail.com',
    description='Noolite communication',
    install_requires=requirements
)
