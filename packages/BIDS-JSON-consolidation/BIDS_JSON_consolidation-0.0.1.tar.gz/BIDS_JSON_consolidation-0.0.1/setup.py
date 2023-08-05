import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BIDS_JSON_consolidation",
    version="0.0.1",
    author="Marco Nardin",
    author_email="27.marco@gmail.com",
    description="A simple package for consolidating BIDS formatted JSON data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marconardin/bids-json",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7, <4'
)
