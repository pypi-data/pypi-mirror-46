import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colabtools",
    version="0.0.1",
    author="zuuuhkrit",
    author_email="zuuuhkrit@gmail.com",
    description="Tools to work with colab from google",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zuuuhkrit/colabtools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
