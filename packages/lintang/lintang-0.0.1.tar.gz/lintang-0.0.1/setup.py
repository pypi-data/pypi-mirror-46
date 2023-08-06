import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lintang",
    version="0.0.1",
    author="Liokta Bagaskara",
    author_email="shiroasasin@gmail.com",
    description="The little arrya",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/liokta/arrya",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)