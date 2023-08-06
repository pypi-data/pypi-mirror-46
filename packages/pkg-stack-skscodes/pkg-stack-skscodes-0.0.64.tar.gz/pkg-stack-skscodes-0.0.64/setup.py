import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pkg-stack-skscodes",
    version="0.0.64",
    author="suyog k sethia",
    author_email="ssethia86@gmail.com",
    description="It is documented package 'pkg_stack' which provides feature 'stack' functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)