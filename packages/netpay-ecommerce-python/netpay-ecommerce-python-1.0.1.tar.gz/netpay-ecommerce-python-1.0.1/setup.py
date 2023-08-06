import setuptools
with open("readme.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='netpay-ecommerce-python',  
     version='1.0.1',
     author="Netpay",
     author_email="info@netpay.com.mx",
     description="A Python scripts for consume eccomerce Api",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )