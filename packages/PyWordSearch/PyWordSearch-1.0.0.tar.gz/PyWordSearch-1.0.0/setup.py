from setuptools import setup

def readme():
	with open('README.md') as f:
		README = f.read()
	return README

setup(
	name = "PyWordSearch",
	version = '1.0.0',
	description = "A python package that solves word searches.",
	long_description = readme(),
	long_description_content_type = "text/markdown",
	url = 'https://github.com/clarkthepooh/pysearch/',
	author = 'Clark Mattoon',
	license='MIT',
	classifiers = [
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.7"
	],
	packages = ['searchproject'],
	include_package_data=True
)