import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
     name='varunmurthy',  
     version='0.0.2',
     author="Varun Murthy",
     author_email="murthy@berkeley.edu",
     description="Mr. Murthy's professional information at your fingertips.",
     long_description=long_description,
    long_description_content_type="text/markdown",
     url="https://github.com/Murthy1999/varunmurthy",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
         "Operating System :: OS Independent",
     ],
 )