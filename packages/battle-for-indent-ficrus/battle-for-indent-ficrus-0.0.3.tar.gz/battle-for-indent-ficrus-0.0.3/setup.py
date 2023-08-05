import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="battle-for-indent-ficrus",
    version="0.0.3",
    author="ficrus",
    author_email="eaglemango@gmail.com",
    description="Open-source strategy game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ficrus/battle-for-indent",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
