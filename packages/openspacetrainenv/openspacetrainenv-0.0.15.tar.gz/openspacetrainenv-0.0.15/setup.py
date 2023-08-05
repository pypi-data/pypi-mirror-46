import setuptools
from pip._internal.download import PipSession
from pip._internal.req import parse_requirements

print(setuptools.find_packages(include=['src', 'src.*']))

with open("README.md", "r") as fh:
    long_description = fh.read()


install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]


setuptools.setup(
    name="openspacetrainenv",
    version="0.0.15",
    author="OpenSpace",
    description="The OpenSpace train environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.ugent.be/OpenSpace-DP/train_env",
    packages=setuptools.find_packages(include=['src', 'src.*']),
    install_requires=reqs,
    package_dir={'src': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
