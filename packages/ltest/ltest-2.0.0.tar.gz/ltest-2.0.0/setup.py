import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ltest',
    version='2.0.0',
    author='William Mak',
    author_email='william@wmak.io',
    description='A package for lazy people who test things',
    long_description=long_description,
    url='https://github.com/wmak/ltest',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
)
