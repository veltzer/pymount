import setuptools


def get_readme():
    with open("README.rst") as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pymount",
    version="0.0.11",
    packages=[
        "pymount",
    ],
    # from here all is optional
    description="module to help you mount and unmount file systems",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        "pymount",
        "mount",
        "umount",
        "partition",
    ],
    url="https://veltzer.github.io/pymount",
    download_url="https://github.com/veltzer/pymount",
    license="MIT",
    platforms=[
        "python3",
    ],
    install_requires=[
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
