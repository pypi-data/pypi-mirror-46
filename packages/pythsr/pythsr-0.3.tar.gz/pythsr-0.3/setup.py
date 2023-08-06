import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setuptools.setup(
    name='pythsr',
    version='0.3',
    description='A collection of python utils for personal use',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/thsr/pythsr',
    author='thsr',
    author_email='437808@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)