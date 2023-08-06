import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='pgnow',  
     version='0.2.4',
     author="Fede Kamelhar",
     author_email="fkamelhar@gmail.com",
     description="A Tool to Integrate PG8000 into your application",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/TrAsGo/pgnow",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
