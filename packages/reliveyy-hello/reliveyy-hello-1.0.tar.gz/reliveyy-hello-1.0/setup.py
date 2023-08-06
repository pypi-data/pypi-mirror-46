import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="reliveyy-hello",
    version="1.0",
    scripts=[],
    author="Yang Yang",
    author_email="reliveyy@gmail.com",
    description="My first pip package just print hello",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
