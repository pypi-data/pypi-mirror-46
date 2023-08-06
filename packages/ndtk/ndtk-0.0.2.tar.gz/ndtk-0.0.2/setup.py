import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ndtk",
    version="0.0.2",
    author="georgethrax",
    author_email="pyruby@163.com",
    description="Novelty Detection Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/georgethrax/ndtk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[]
)