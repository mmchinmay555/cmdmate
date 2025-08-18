from setuptools import setup, find_packages

setup(
    name="cmdmate",               # pip package name
    version="0.1.0",
    description="cmdmate : Your AI-powered terminal command assistant",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mmchinmay555/",
    author="Chinmay Rao",
    packages=find_packages(include=["client", "client.*"]),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.32.0"
    ],
    entry_points={
        "console_scripts": [
            "cmdmate=client.cmdmate_cli:main",  # this makes `cmdmate` CLI available
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)