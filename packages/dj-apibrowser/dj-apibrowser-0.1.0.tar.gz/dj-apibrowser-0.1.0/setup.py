from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding = 'utf-8') as f:
	long_description = f.read()

setup(
	name = 'dj-apibrowser',
	version = '0.1.0',
	description = 'Generic GUI for any RESTful API',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://gitlab.com/LEW21/dj-apibrowser',
	author = "Linus Lewandowski",
	author_email = "linus@lew21.net",
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Framework :: Django',
		'Framework :: Django :: 2.0',
		'Framework :: Django :: 2.1',
		'Framework :: Django :: 2.2',
	],
	keywords = 'rest api browser',
	py_modules = [
		'dj_apibrowser',
	],
	zip_safe = True,
	install_requires = [],
	extras_require = {},
)
