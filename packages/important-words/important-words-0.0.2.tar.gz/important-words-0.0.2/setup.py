import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="important-words",
version="0.0.2",
    author="Tan Kim Yong",
    author_email="kimyong95@gmail.com",
    description="Find important words from a sentence.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        "torch",
        "spacy",
        "numpy",
        "sklearn",
    ],
)
