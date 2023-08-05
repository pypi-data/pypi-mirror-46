import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ecapture",
    version="0.1.8",
    scripts=['ecapture/ecapture.py'],
    description="Webcams made easy",
    install_requires=["opencv-python","scikit-image==0.14.2"],
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/YFOMNN/ecapture",
    author="Mohammmed Yaseen",
    author_email="hmyaseen05@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["ecapture"],
    include_package_data=True,
)
