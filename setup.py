import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='pymount',
    version='0.0.8',
    description='module to help you mount and unmount file systems',
    long_description='programmatic API to /proc/partitions and /proc/mounts',
    url='https://veltzer.github.io/pymount',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='pymount mount umount partition',
    packages=setuptools.find_packages(),
)
