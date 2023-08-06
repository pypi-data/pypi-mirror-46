import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pySMP",
	version="0.1.1",
	author="King Abdullah Petroleum Studies and Research Center",
	author_email="ktab@kapsarc.org",
	description="KTAB",
	long_description=long_description,
	long_description_conent_type="text/markdown",
	url="https://github.com/kapsarc/pySMP",
	packages=['pySMP'],
	package_dir={'pySMP': 'pySMP'},
	package_data={'pySMP': ['lib/*.so', 'lib/*.dll', 'lib/*.dylib']},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	]
)