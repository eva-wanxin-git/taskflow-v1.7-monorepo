"""
Industrial Dashboard - Setup Script

用于打包和分发
"""
from setuptools import setup, find_packages

setup(
    name="industrial-dashboard",
    version="1.0.0",
    description="工业美学风格的任务监控 Dashboard",
    author="AI Task Automation Team",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

