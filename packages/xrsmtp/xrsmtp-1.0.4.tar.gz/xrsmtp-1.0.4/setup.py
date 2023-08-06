import setuptools

with open("README.md","r") as f:
   long_description = f.read()

setuptools.setup(
   name="xrsmtp",
   version="1.0.4",
   author="XploitsR Author (solomon narh)",
   author_email="solomonnarh97062@gmail.com",
   license="MIT",
   description="XploitsR | XRSmtp is a module for fetching the details of any SMTP provider for your development or personal use.",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/XploitsR/XRSmtp",
   packages=setuptools.find_packages(),
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
)
