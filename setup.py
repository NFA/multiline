import setuptools

with open("README.rst", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="multiline", 
    version="0.0.1",
    author="Fredrik Nyström",
    author_email="nfa106@gmail.com",
    description="Module to facilitate data transmission from a WTW MultiLineIDS portable meter.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/NFA/multiline",
    packages=setuptools.find_packages(include=["multiline"]),
    install_requires=[
        "pyserial",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Classifier: Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
)