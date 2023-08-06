import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nester_hpp",
    version="1.0.1",
    author="hpp712",
    author_email="chan.1201@163.com",
    description="A simple printer of nested lists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/manage/projects/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
