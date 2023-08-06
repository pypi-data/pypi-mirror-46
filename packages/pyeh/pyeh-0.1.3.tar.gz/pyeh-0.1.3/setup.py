import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pyeh",
    version="0.1.3",
    author="Konrad P",
    description="A small SDK for EH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/konradp/pyeh",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
