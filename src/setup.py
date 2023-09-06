import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylapi",
    version="0.11",
    author="Jacky Ko",
    author_email="",
    description="PyLapi - Python Lightweight API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackyko8/pylapi",
    project_urls={
        "Bug Tracker": "https://github.com/jackyko8/pylapi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "package"},
    packages=setuptools.find_packages(where="package"),
    python_requires=">=3.7",
)
