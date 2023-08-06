import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='openproteindesign',
     version='0.1dev',
     author="Dominik Lemm",
     author_email="lemm92.d@gmail.com",
     description="A general purpose Protein Design Package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/openproteindesign/openproteindesign",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
