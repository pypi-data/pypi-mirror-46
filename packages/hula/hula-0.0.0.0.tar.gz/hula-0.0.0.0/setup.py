import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hula",
    version="0.0.0.0",
    author="Robert Bassett",
    author_email="robert.bassett.coder@gmail.com",
    description="Experimental learning methods. The first appearance of these methods.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",

    ],
)
