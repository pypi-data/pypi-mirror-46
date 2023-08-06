import setuptools

with open("README.md","r") as f:
   long_description = f.read()

setuptools.setup(
   name="xrdownloader",
   version="1.0.2",
   author="XploitsR Author (solomon narh)",
   author_email="solomonnarh97062@gmail.com",
   license="MIT",
   description="XploitsR | XRDownloader is a module for faster downloading of files.",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/XploitsR/XRDownloader",
   packages=setuptools.find_packages(),
   install_requires=[
       'urllib3',
       'certifi',
   ],
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
)
