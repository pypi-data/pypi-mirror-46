import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data-entry-demo",
    version="0.0.1",
    author="adam",
    author_email="adam.kehoe@opexanalytics.com",
    description="package to demo CHR data entry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
