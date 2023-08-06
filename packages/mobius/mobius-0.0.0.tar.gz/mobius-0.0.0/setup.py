#!/usr/bin/env python
import setuptools

import mobius


install_requires = (
)

setuptools.setup(
    name="mobius",
    version=mobius.VERSION,
    author="Daniel Edgy Edgecombe",
    author_email="swinging.clown@gmail.com",
    url="https://github.com/EdgyEdgemond/mobius",
    include_package_data=True,
    packages=setuptools.find_packages(include=("mobius*",)),
    install_requires=install_requires,

    extras_require={
        "test": (
            "freezegun",
            "pytest>=4.5.0",
            "pytest-aiohttp",
            "pytest-asyncio",
            "pytest-benchmark",
            "pytest-cov",
            "pytest-random-order",
            "pytest-xdist",
        ),
        "dev": (
            "flake8",
            "flake8-commas",
            "flake8-isort",
            "flake8-mypy",
            "flake8-quotes",
            "isort>=4.3.15",
            "pytest-cov",
        ),
        "release": (
            "bumpversion",
        ),
    },
)
