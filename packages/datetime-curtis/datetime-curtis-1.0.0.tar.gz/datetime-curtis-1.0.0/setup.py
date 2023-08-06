from setuptools import setup, find_packages

setup(

	name='datetime-curtis',
	version='1.0.0',
	description='a datetime project',
	url='https://github.com/odhiambocuttice/myfirstproject',
	author='odhiambo cuttice',
	author_email='odhiambocuttice@gmail.com',

	classifiers=[
         
         'License :: OSI Approved :: MIT License',
         'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
	],

	keywords ='datetime setuptools development',

	packages =find_packages(),
	python_requires ='>=3.6',
	install_requires=['requests'],

	)
