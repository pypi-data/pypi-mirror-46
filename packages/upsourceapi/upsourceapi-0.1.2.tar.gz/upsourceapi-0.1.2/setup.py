import os

from setuptools import setup, find_packages

local_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(local_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="upsourceapi",
    version="0.1.2",
    description="Upsource API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bioinf/alt-code",
    author="stepik.org",
    author_email="ivan.magda@stepik.org",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    keywords=["upsource", "api"],
    python_requires='>=3.0, <4',
    install_requires=["dataclasses"],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    zip_safe=False,
    entry_points={
        "console_scripts": ["upsourceapi=upsourceapi.__main__:main"]
    }
)
