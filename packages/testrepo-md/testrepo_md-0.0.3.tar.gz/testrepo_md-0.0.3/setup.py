import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testrepo_md",
    version="0.0.3",
    author="Marilia",
    description="Library for testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbarandas/testrepo_md/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
