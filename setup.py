import os

import pkg_resources
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'ftfy',
    'regex',
    'tqdm',
    "model-tools @ git+https://github.com/brain-score/model-tools",
    "numpy",
    'xarray',
    "result_caching @ git+https://github.com/mschrimpf/result_caching",
    'torch',
    'torchvision',
]
    
setup(
    name="clip",
    py_modules=["clip"],
    version="1.0",
    description="",
    author="OpenAI",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requirements,
    include_package_data=True,
    extras_require={'dev': ['pytest']},
)
