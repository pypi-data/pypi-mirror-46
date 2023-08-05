import setuptools
  
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dms2dec",
    version="0.01",
    author="",
    author_email="",
    description="DMS to decimal. Convert degrees minutes seconds to decimal latitude/longitude",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
    install_requires=[],
)

