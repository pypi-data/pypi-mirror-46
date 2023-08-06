import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acs_wrapper",
    version="1.0.3",
    author="Diego Pinheiro",
    author_email="diegompin@gmail.com",
    description="A wrapper for the American Community Survey Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diegompin/american-community-survey",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
          'pandas',
      ],
)