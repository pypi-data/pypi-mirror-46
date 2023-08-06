import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taobao-sdk-top",
    version="0.0.1",
    author="silin",
    author_email="silinwork@gmail.com",
    description="taobao sdk for python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sl40/taobao-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
