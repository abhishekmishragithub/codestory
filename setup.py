# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codestory",
    version="0.1.0",
    author="Abhishek Mishra",
    author_email="abhi.mishra922@gmail.com",
    description="A cli tool for generating conventional commit messages using LLM models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/codestory",
    packages=find_packages(),
    install_requires=[
        "click",
        "gitpython",
        "python-dotenv",
        "outlines",
        "pydantic",
        "transformers",
        "openai",
        "google-generativeai",
        "anthropic",
        "groq",
        "requests"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "codestory=codestory.cli:main",
        ],
    },
)