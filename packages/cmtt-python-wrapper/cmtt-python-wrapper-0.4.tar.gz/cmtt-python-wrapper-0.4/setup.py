import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmtt-python-wrapper",
    version="0.4",
    author="nenanimalsya",
    author_email="nenanimalsya@example.com",
    description="Python wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nenanimalsya/cmtt-python-wrapper/",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests',
      ],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    include_package_data=True,
)