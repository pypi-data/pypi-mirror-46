import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlend-probability",
    version="0.1",
    author="Foxan Ng",
    author_email="foxan.ng@gmail.com",
    description="Gaussian and Binomial distribution",
    long_description=long_description,
    packages=setuptools.find_packages(),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "matplotlib>=3.0.3",
    ],
)