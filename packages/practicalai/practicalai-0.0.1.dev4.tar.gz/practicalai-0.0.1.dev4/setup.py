from setuptools import setup, find_packages

# Long description will be README.md
with open("README.md", "r") as fp:
    long_description = fp.read()

# Read requirements
requirements = [package for package in open(
    "requirements.txt").read().split("\n") if package]

setup(
    name="practicalai",
    version="0.0.1.dev4",
    author="Goku Mohandas",
    author_email="gokumd@gmail.com",
    description="practicalAI · A practical approach to machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/practicalAI/practicalai",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
