import re
from setuptools import setup


def find_version(filename):
    """
    Search for assignment of __version__ string in given file and
    return what it is assigned to.
    """
    with open(filename, "r") as filep:
        version_file = filep.read()
        version_match = re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
        )
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")


setup(
    name="tweetmagick",
    version=find_version("tweetmagick/tweetmagick.py"),
    description="Create images that look like tweets",
    long_description=open("README.rst", "r").read(),
    url="https://github.com/Szero/tweetmagick",
    license="ISC",
    author="Szero",
    author_email="singleton@tfwno.gf",
    packages=["tweetmagick"],
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[l.strip() for l in open("requirements.txt").readlines()],
)
