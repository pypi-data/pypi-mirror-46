import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discountr-client",
    version="0.0.2",
    author="Turkalp Burak KAYRANCIOGLU",
    author_email="bkayranci@gmail.com",
    description="Discountr API Client",
    long_description=long_description,
    url="https://gitlab.com/discountr_info/api-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
