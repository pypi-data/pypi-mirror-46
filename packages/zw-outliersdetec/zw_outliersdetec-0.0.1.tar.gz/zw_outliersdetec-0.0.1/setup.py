from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="zw_outliersdetec",
    version="0.0.1",    #第一版
    author="Zuo Wei",
    author_email="zw@my.swjtu.edu.cn",
    description="A small outliers-detection package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vidiewei",
    packages=find_packages(),
    #include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)