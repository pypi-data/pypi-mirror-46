import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torchwisdom",
    version="0.0.2-dev1",
    author="Lalu Erfandi Maula Yusnu",
    author_email="nunenuh@gmail.com",
    description="High Level API for PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nunenuh/torchwisdom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)