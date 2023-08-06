import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='experimentsLogReader',  
     version='2.2.0',
     author="Jānis Šteinbergs",
     author_email="janis.akmenskalns@gmail.com",
     description="Log file reader for Radio Astronomy",
     long_description=long_description,
     keywords=['VIRAC'],
   long_description_content_type="text/markdown",
     url="https://github.com/sklandrausis/ExperimentsLogReader",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
