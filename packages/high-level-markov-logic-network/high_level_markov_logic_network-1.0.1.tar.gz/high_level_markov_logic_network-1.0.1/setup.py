import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="high_level_markov_logic_network",
    version="1.0.1",
    author="Sebastian Koralewski",
    author_email="seba@cs.uni-bremen.de",
    description="Provides high level functions to access the main functionality of pracmln.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/code-iai/high-level-markov-logic-network",
    packages=setuptools.find_packages(exclude=("test",)),
    install_requires=['pracmln==1.2.3'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)