import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="experiment-replay",
    version="0.0.1",
    author="Nicolas Patry",
    author_email="patry.nicolas@protonmail.com",
    description="Make running, replaying experiments easier either on Pytorch or Tensorflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Narsil/experiment_replay",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
