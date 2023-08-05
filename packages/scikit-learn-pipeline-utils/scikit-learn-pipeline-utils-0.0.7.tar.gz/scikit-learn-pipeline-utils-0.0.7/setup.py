import pathlib
from sklearn_pipeline_utils import __version__
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="scikit-learn-pipeline-utils",
    version= __version__,
    description="Custom Pipeline Transformers for Sklearn Pipelines",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/deltahedge1/scikit-learn-pipeline-utils",
    author="Ish Hassan",
    author_email="ishassan90@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["sklearn_pipeline_utils"],
    include_package_data=True,
    install_requires=["scikit_learn", "pandas"],
    data_files = [("", ["LICENSE"])]
)