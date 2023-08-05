from setuptools import setup

long_description = open('README.md').read()

setup(
	name='sky-remote',
	version='1.0',
	description='Python module to send remote control commands to a Sky TV box',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/WoolDoughnut310/sky-remote',
	author='J. Nma',
	author_email='wooldoughnutspi@outlook.com',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Libraries',
		'Programming Language :: Python :: 3'
	],
	keywords='sky-remote python3 tcp/ip',
	py_modules='sky_remote',
	python_requires='>=3'
)