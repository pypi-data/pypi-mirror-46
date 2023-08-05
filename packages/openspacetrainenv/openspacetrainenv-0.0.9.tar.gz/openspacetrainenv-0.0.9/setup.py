import setuptools

print(setuptools.find_packages())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openspacetrainenv",
    version="0.0.9",
    author="OpenSpace",
    description="The OpenSpace train environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.ugent.be/OpenSpace-DP/train_env",
    packages=['train_env'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
