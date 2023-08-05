"""Setup script for drf-insights-pagination."""

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="drf-insights-pagination",
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    author="Cloudigrade Team",
    author_email="doppler-dev@redhat.com",
    description="Provides pagination class that adheres to Insights IPP-12.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="djangorestframework drf pagination insights ipp-12",
    license="GPLv3",
    url="https://gitlab.com/cloudigrade/libraries/drf-insights-pagination",
    packages=find_packages(),
    install_requires=["djangorestframework"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
