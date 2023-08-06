import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dices",
    version="0.0.1",
    author="V3L",
    author_email="p@v3l.cz",
    description="A handful of dices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skooda/pyDices",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
