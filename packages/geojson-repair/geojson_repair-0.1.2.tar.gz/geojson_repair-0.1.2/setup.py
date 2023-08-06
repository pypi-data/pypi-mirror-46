import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geojson_repair",
    version="0.1.2",
    author="Jacob Rosbrow",
    author_email="jake@rosbrow.org",
    description="Repair utilities for geojson objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrosbrow/geojson_repair",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"geojson_repair": "geojson_repair"}
)