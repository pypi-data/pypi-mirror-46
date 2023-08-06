import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="description2process",
    version="0.1.1",
    author="Simeon & Niels",
    author_email="author@example.com",
    description="Library for constructing a process model given the process description. Deep learning techniques are implmented as much as possible.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        'neuralcoref',
        'benepar',
        'allennlp',
        'graphviz',
        'spacy',
        'tensorflow',
        'tensor2tensor'
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
