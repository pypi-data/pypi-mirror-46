import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='nexus1000v',
     version='1.2',
     author="Vinay Pillutla",
     author_email="vinaypillutla@yahoo.in",
     description="Package to perform operations on Cisco Nexus 1000v",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/vinaypillutla/nexus1000v.git",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )
