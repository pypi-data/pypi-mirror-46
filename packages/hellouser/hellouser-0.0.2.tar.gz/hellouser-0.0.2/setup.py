import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()
	
setuptools.setup(
    name="hellouser",
    version="0.0.2",
    author="Nagalatha",
    author_email="nagalatha@gmail.com",
    description="Say hello!",
    py_modules=["hellouser"],
    package_dir={'' : 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohitaradhya",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
