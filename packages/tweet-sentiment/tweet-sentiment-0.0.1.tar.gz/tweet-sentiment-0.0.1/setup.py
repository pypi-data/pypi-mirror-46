import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tweet-sentiment",
    version="0.0.1",
    author="Moe Antar , Eric Schibli",
    author_email="moe.antar@hotmail.com",
    description="A small package that allows the cleaning and sentiment scoring of tweets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)