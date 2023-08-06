from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="jdict",
    version="1.0.0",
    description="Dictionary extended with convenience methods that depend heavily on dictionaries being ordered by insertion order.",
    url="https://github.com/jonathangjertsen/jdict",
    author="Jonathan Reichelt Gjertsen",
    author_email="jonath.re@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["jdict"],
    license="MIT",
    zip_safe=False,
)
