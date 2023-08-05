import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="data-generator-postgresql-pkg",
	version="0.0.0.6",
	author="Tarasenko Stepan",
	author_email="st.a.tarasenko@gmail.com",
	description="Data generator for postgres",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://example.com",
	packages=setuptools.find_packages(),
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)