from setuptools import setup, find_packages


setup(
    name="unpacked",
    version="0.0.1",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nikita Tsvetkov",
    author_email="nikitanovosibirsk@yandex.com",
    python_requires=">=3.6.0",
    url="https://github.com/nikitanovosibirsk/unpacked",
    license="Apache 2",
    packages=find_packages(exclude=("tests",)),
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
    ],
)
