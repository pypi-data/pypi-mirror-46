from setuptools import setup

setup(name='Othello_Python',
	version='0.1',
	description='A Python implementation of Othello',
	download_url='https://github.com/danieljburns143/Othello_Python/archive/0.1.tar.gz',
	author='Daniel Burns',
	author_email='danieljburns143@gmail.com',
	license='MIT',
	packages=['Othello_Python'],
	zip_safe=False,
	entry_points={
		'console_scripts': ['Othello_Python=Othello_Python.othello_execution:main']
	})
