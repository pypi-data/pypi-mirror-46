from setuptools import setup

setup(
    name="IPythonReverser",
    version="0.1",
    packages=["ipython_reverser"],
    license="MIT",
    author="Sebastian Witowski",
    author_email="sebastian@switowski.com",
    url="http://www.github.com/switowski/ipython-reverser",
    description="IPython magic to reverse a string",
    long_description=open("README.rst").read(),
    keywords="ipython reverser reverse",
    install_requires = ['ipython'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Framework :: IPython",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
