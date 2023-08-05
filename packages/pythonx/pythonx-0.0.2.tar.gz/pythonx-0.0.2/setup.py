import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythonx", # 包名
    version="0.0.2",
    author="Jins Yin",
    author_email="jinsyin@gmail.com",
    description="Python X",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jinsyin/x/tree/master/pythonx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
