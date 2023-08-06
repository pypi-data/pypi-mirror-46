import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rufmich",
    version="1.0.6",
    author="daseinpwt",
    author_email="daseinpwt@gmail.com",
    description="A Python server implementaion of JSON-RPC 2.0 over HTTP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daseinpwt/rufmich",
    packages=setuptools.find_packages(),
    install_requires=[
        'flask',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)