import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reindeer",
    version="0.1.2",
    author="Nils Kleber",
    author_email="n.kleber@usu.de",
    description="Reindeer ist eine Python Bibliothek um durch Verwendung des DEER-Frameworks, CSV-Datensätzen mit zusätzlichen Informationen aus LinkedData anzureichern.",
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
