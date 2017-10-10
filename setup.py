import setuptools

setuptools.setup(
    name='pymount',
    version='0.0.8',
    description='module to help you mount and unmount file systems',
    long_description='programmatic API to /proc/partitions and /proc/mounts',
    url='https://github.com/veltzer/pymount',
    download_url='https://github.com/veltzer/pymount',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    platforms=['python3'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='pymount mount umount partition',
    packages=setuptools.find_packages(),
)
