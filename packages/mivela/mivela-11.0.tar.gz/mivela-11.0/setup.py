import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mivela",
    version="11.0",
    author="Amateur Bandit",
    author_email="amateurbandit@yandex.com",
    description="A small package for water drinking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/testiramsve/mivela",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
