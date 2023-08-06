import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pythsr',
    version='0.1',
    description='A collection of python utils for personal use',
    long_description=long_description,
    long_description_content_type="text/markdown",
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