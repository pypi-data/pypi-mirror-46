from setuptools import setup


setup(
    name='WoodenCrypto',
    version='0.0.8',
    author='zhanghaoran',
    author_email='haoranzeus@gmail.com',
    url='https://www.zhanghaoran.cc',
    packages=['WoodenCrypto', ],
    install_requires=[
        'pycrypto', 'rsa'
    ])
