import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slacksdk",
    version="0.0.1a",
    author="Thanakrit Juthamongkhon",
    author_email="thanakrit.ju.work@gmail.com",
    description="A minimal slack sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thanakritju/python-slack-events-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)