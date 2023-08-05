import setuptools

print(setuptools.find_packages(include=['src', 'src.*']))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openspacetrainenv",
    version="0.0.10",
    author="OpenSpace",
    description="The OpenSpace train environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.ugent.be/OpenSpace-DP/train_env",
    packages=list(map(lambda x: x.replace('src', 'train_env'), setuptools.find_packages(include=['src', 'src.*']))),
    package_dir={'train_env': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
