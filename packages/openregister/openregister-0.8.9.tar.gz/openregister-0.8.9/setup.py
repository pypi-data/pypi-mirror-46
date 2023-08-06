from setuptools import setup, find_packages
import os
import sys
from version import get_version


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


# Only install black on Python 3.6 or higher
maybe_black = []
if sys.version_info > (3, 6):
    maybe_black = ["black"]

setup(
    name="openregister",
    version=get_version(),
    description="Publishing tools for GOV.UK style registers",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Paul Downey",
    author_email="paul.downey@whatfettle.com",
    license="MIT",
    url="https://github.com/psd/openregister",
    packages=find_packages(exclude="tests"),
    package_data={"openregister": ["templates/*.html"]},
    include_package_data=True,
    install_requires=[
        "click==7.0",
        "click-default-group==1.2",
        "PyYAML==3.13",
        "requests==2.22.0",
        "Sanic==0.7.0",
        "tempdir==0.7.1",
    ],
    entry_points="""
        [console_scripts]
        openregister=openregister.cli:cli
    """,
    setup_requires=["pytest-runner"],
    extras_require={
        "test": [
            "coverage>=4.5.3",
            "flake8>=3.7.7",
            "pytest>=4.0.2",
            "python-coveralls>=2.9.1",
            "twine>=1.13.0",
        ]
        + maybe_black
    },
    tests_require=["openregister[test]"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
