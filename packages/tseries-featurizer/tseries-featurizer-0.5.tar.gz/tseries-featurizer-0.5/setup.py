import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

with open('requirements.txt', 'r') as file:
	requirements = file.read().split('\n')

print(requirements)

setuptools.setup(

	name='tseries-featurizer',

	version='0.5',

	scripts=['ts-featurizer'],

	author="Joanes Plazaola",

	author_email="joanes.plazamadi@gmail.com",

	install_requires=requirements,

	description="A time series featurizer.",

	long_description=long_description,

	long_description_content_type="text/markdown",

	url="https://bitbucket.org/joanesplazaola/time-series-featurizer",

	packages=setuptools.find_packages(),

	classifiers=[

		"Programming Language :: Python :: 3",

		"License :: OSI Approved :: MIT License",

		"Operating System :: OS Independent",

	],

)
