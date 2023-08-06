from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pflogger",
    version='0.0.2',
    description="Configuration of python logging handler for Perfee.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/perfeelab/pflogger",
    author='ClaireHuang',
    author_email='clairehf@163.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)