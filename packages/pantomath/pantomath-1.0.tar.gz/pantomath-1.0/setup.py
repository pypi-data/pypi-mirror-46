from setuptools import setup, find_packages


setup(
	name='pantomath',
	version='1.0',
	description='I want to know everything',
	license='GNU AGPLv3',
	url='',
	author='Idin',
	author_email='py@idin.ca',

	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
	packages=find_packages(exclude=("jupyter_tests", ".idea", ".git")),
	install_requires=[

	],
	python_requires='~=3.6',
	zip_safe=True
)