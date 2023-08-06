import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lonhand",
    version="0.1",
    author="rp3tya",
    author_email="rpetya@hotmail.com",
    description="LonHand client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rp3tya/LonHand",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="lonhand relay",
)
