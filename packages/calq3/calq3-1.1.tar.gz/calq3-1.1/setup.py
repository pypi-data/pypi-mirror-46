import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='calq3',  

     version='1.01',

     scripts=['src/calq3'] ,

     author="Nanjiang Shu",

     author_email="nanjiang.shu@gmail.com",

     description="A script to calculate the Q3 score of secondary structure prediction",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://github.com/nanjiang/calQ3-simple",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )
