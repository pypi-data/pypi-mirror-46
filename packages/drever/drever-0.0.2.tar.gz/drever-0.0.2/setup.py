import setuptools

import drever

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drever",
    version=drever.__version__,
    author="Tobias Baumann",
    author_email="tobias.baumann@elpra.de",
    description="A framework for handling testvectors " +
                "within an HDL testbench.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Elpra/drever-framework/drever",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License " +
        "v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
