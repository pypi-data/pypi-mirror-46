import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='l-graph',
    version='0.2.2',
     author="Dmitry Rudanov",
     author_email="rudanov.d@gmail.com",
     description="Python module for working with L-graphs",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/rudanov/lgraph",
     packages=['lgraph'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )