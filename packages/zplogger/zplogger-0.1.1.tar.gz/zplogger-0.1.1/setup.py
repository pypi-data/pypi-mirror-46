import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="zplogger",
    version="0.1.1",
    author="zjhiphop",
    author_email="zjhiphop@gmail.com",
    description="ZPower Logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zjhiphop/logger",
    packages=setuptools.find_packages(),
    install_requires=['requests>=2.21.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platforms="any",
)