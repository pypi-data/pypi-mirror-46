import setuptools
from pathlib import Path

DIR = Path(__file__).parent
README = DIR/'README.md'

setuptools.setup(
    name="hashbang",
    version="0.0.1",
    author="Maurice Lam",
    author_email="mauriceprograms@gmail.com",
    description="Create command line arguments with just an annotation",
    long_description=README.read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/mauricelam/hashbang",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: System :: Shells",
    ],
)
