import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sonofabatch",
    version="0.0.2",
    author="Mike Ortman",
    author_email="mikeortman@gmail.com",
    description="A very simple and really fast batch processing toolkit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/mikeortman/sonofabatch",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    py_modules=["faker", "asyncio"],
)
