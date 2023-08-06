from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="Tempus.py",
    version="1.1.0",
    description="Simple date handler",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yojona/tempus.py",
    author="Jonathan Ayala",
    author_email="yojona@msn.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=["tempus"],
    include_package_data=True
)
