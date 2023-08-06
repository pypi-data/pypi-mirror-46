import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="piudb",
    version="0.0.0",
    author="Wang Pei",
    author_email="1535376447@qq.com",
    description="This is a simple package, which can be used as a substitute of database.\nUnlike a database, this one doesn't store records, but store objects directly .",
    long_description=None,
    long_description_content_type="text/markdown",
    url="https://github.com/Peiiii/xiudb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)