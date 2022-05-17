from setuptools import setup, find_namespace_packages

setup(
    name="py-info-machine",
    version="1.0",
    packages=find_namespace_packages(),
    install_requires=[
        "tqdm==4.64.0"
    ]
)