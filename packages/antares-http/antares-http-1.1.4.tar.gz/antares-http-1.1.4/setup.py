import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="antares-http",
    version="1.1.4",
    author="Antares Support Team",
    author_email="support@antares.id",
    description="A Python Library to simplify connection to Antares IoT Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antaresdocumentation/antares-python",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

