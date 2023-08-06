import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    name="astep_forms_utils",
    version="0.2.6",
    author="Casper Weiss Bang",
    author_email="master@thecdk.net",
    description="A package for utilities regarding the aSTEP 2019 rendering architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://daisy-git.cs.aau.dk/aSTEP-2019/python_form_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
