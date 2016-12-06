import setuptools

setuptools.setup(
    name='mount',
    version='0.0.1',
    description='module to help you mount and unmount file systems',
    long_description='programmatic API to /proc/partitions and /proc/mounts',
    url='https://veltzer.github.io/mount',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='GPL3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='mount umount partition',
    package_dir={'':'src'},
    packages=setuptools.find_packages('src'),
)
