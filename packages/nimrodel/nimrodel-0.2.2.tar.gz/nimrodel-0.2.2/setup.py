import setuptools
import importlib

module = importlib.import_module(setuptools.find_packages()[0])


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=module.name,
    version=".".join(str(n) for n in module.version),
    author="Johannes Krattenmacher",
    author_email="python@krateng.dev",
    description="Bottle.py wrapper to make python objects accessible via HTTP API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krateng/" + module.name,
    packages=setuptools.find_packages(),
	include_package_data=True,
	package_data={module.name:["res/apiexplorer.pyhp"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
