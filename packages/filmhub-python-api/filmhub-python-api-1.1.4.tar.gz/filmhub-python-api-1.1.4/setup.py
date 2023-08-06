import setuptools

with open("README.md", "r") as fh:

	long_description = fh.read()

setuptools.setup(

	 name='filmhub-python-api',  

	 version='1.1.4',

	 packages=['filmhub_api'],

	 author="Henrik Norin",

	 author_email="henrik.norin@filmhubsoftware.com",

	 description="A Python API for controlling FilmHUB fast film delivery software",

	 long_description=long_description,

	 long_description_content_type="text/markdown",

	 url="https://github.com/henriknorin/filmhub-python-api.git",

	 classifiers=[

		 "Programming Language :: Python :: 2",

		 "License :: OSI Approved :: MIT License",

		 "Operating System :: OS Independent",

	 ],

 )