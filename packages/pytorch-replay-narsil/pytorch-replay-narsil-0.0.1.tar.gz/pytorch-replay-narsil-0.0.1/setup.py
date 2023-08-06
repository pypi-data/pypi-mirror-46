import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytorch-replay-narsil",
    version="0.0.1",
    author="Nicolas Patry",
    author_email="patry.nicolas@gmail.com",
    description="Make running, replaying experiments packaging models easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Narsil/pytorch_replay",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
