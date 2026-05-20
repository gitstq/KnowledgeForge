#!/usr/bin/env python3
"""
KnowledgeForge - 轻量级本地AI知识库构建引擎
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="knowledge-forge",
    version="1.0.0",
    author="KnowledgeForge Team",
    author_email="hello@knowledgeforge.dev",
    description="轻量级本地AI知识库构建引擎 | Lightweight Local AI Knowledge Base Building Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/knowledge-forge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "knowledge-forge=main:main",
            "kforge=main:main",
        ],
    },
    keywords="knowledge-base, rag, ai, search, nlp, semantic-search, cli, local-ai",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/knowledge-forge/issues",
        "Source": "https://github.com/yourusername/knowledge-forge",
    },
)
