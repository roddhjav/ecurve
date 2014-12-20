from setuptools import setup

setup(name='ecurve',
	version='1.0',
	description='cryptographic primitives on elliptic curves',
	author='Alexandre Pujol & Chemin Maxime',
	license='GPL',
	packages=['ecurve'],
	install_requires=['pycrypto',],
	zip_safe=False)
