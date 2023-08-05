import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Encryption",
    version="0.0.1",
    author="Noah Siegel",
    author_email="nasiegel8@gmail.com",
    description="Basic text transformations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nasiegel8/Encryptions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
