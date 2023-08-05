import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aquacroppy",
    version="0.0.0.1",
    author="Noah Spahn",
    author_email="author@example.com",
    description="AquaCrop Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noah-de/aquacroppy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
