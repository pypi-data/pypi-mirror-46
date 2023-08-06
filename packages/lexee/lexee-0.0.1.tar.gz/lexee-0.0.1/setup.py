from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lexee",
    version="0.0.1",
    author="Dialect Software LLC",
    author_email="support@dialectsoftware.com",
    description="Pylingo interpreter",
    long_description="Lexee is an extensible interpreter for the pylingo grammar built using protolingo",
    long_description_content_type="text/markdown",
    url="https://github.com/dialectsoftware/lexee",
    packages= find_packages(),
    install_requires=[
          'Pykka',
          'jinja2',
          'PyYAML',
          'Protolingo',
          'Pylingo'
      ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)