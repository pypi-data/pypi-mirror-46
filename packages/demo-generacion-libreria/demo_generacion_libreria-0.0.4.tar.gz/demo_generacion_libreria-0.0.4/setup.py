import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="demo_generacion_libreria",
    version="0.0.4",
    author="Pablo Suana",
    author_email="pablo.suana@luceit.es",
    description="Module to show how to create a library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pandas'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

