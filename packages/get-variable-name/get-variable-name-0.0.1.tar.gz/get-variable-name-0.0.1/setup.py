import setuptools
with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="get-variable-name",
    version="0.0.1",
    author="Farinnako Adeyanju Victor",
    author_email="ennythan006@gmail.com",
    description="Returns variable name as a string",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sorxcode/get-variable-name",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
