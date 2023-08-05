import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webmontage",
    version="0.0.1",
    author="Dylan Williams",
    author_email="dylan@dylanfw.com",
    description="Web page montage generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dylanfw/webmontage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
