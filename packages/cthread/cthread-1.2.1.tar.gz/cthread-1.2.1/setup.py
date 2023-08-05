import setuptools

with open("README.md", "r") as f:
    longDescription = f.read()

setuptools.setup(
    name="cthread",
    version="1.2.1",
    author="Kieran Sonter",
    author_email="ksonter95@gmail.com",
    description="Python implementation of a thread that can be started, " \
            "stopped, paused, resumed, and reset.",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://github.com/ksonter95/ControllableThread.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)