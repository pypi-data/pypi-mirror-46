import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-sixpi",
    version="0.0.1",
    author="Bing Xia",
    author_email="bing@outlook.com",
    description="Example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/sixpi/pypi-test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)
