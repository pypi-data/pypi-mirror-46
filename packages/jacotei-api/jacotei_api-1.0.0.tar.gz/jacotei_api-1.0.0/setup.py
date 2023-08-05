import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jacotei_api",
    version="1.0.0",
    author="Luis Milanese",
    author_email="luis.milanese@jacotei.com.br",
    description="SDK for consumption of JáCotei Api",
    long_description=long_description,
    url="https://github.com/jacotei/jacotei-api-sdk-python3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
