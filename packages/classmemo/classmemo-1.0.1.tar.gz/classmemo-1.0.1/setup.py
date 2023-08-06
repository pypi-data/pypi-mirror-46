from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="classmemo",
    version="1.0.1",
    description="Memoizer for classes",
    url="https://github.com/jonathangjertsen/classmemo",
    author="Jonathan Reichelt Gjertsen",
    author_email="jonath.re@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["classmemo"],
    license="MIT",
    zip_safe=False,
)
