import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-qbo",
    version="0.3.0",
    author="Sebastian Rutofski",
    author_email="kontakt@sebastian-rutofski.de",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sebrut/python-qbo",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "urllib3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
