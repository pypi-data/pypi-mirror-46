"""
Usage: python setup.py sdist bdist_wheel
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements = fr.read().splitlines()

setuptools.setup(
    name="simple_pyueye",
    version="0.0.6",
    author="Joao Vital",
    author_email="joao.vital@frontwave.com",
	license='3-Clause BSD License',
    description="High-level wrapper for the python bindings package pyueye",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://frontwave.pt/",
    packages=setuptools.find_packages(),
    install_requires=requirements,
)
