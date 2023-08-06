from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="protolingo",
    version="0.0.3",
    author="Dialect Software LLC",
    author_email="support@dialectsoftware.com",
    description="Meta-language Framework",
    long_description="Protolingo is a framework for building custom configuration based DSL(s) in YAML",
    long_description_content_type="text/markdown",
    url="https://github.com/dialectsoftware/protolingo",
    packages= find_packages(),
    install_requires=[
          'Pykka',
          'jinja2',
          'PyYAML'
      ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)