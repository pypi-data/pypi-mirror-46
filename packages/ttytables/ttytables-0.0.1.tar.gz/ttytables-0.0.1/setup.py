import setuptools


with open('README.md', "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="ttytables",
    version="0.0.1",
    author="Oliven",
    author_email="Liuhedong135@163.com",
    description="Print table on Linux or Windows terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liuhedong135/ttytables",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)