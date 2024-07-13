from setuptools import setup, find_packages

setup(
    name="codestory",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "gitpython",
        "python-dotenv",
        "outlines",
        "pydantic",
        "transformers",
    ],
    entry_points={
        "console_scripts": [
            "codestory=codestory.cli:main",
        ],
    },
)