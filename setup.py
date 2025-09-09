from setuptools import setup, find_packages

setup(
    name="cq_cli",
    version="2.3.0",
    license="LICENSE",
    author="Jeremy Wright",
    description="Command Line Interface for executing CadQuery scripts and converting their output to another format.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "cadquery==2.4.0",
        "cadquery_freecad_import_plugin",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black==19.10b0",
            "click==8.0.4",
        ],
    },
    entry_points={
        "console_scripts": [
            "cq-cli=cq_cli.main:main",
        ],
    },
    url="https://github.com/CadQuery/cq-cli",
    project_urls={
        "Bug Tracker": "https://github.com/CadQuery/cq-cli/issues",
    },
)
