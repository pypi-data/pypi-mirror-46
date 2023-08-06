from setuptools import setup


setup(
    name='noolite_api',
    version='0.1.4',
    packages=['noolite_api'],
    url='https://github.com/andvikt/noolite_serial',
    license='BSD',
    author='andrewgermanovich',
    author_email='andvikt@gmail.com',
    description='Noolite communication',
    install_requires=['pyserial', 'aiohttp', 'xmltodict']
)
