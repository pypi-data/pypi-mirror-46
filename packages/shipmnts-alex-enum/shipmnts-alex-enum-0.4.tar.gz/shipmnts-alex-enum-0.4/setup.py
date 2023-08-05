import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='shipmnts-alex-enum',  
     version='0.4',
     author="Charmi Chokshi",
     author_email="charmi@shipmnts.com",
     description="An Enum (currency, freight terms, and weight UOM) utility package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/charmiShipmnts/shipmnts-alex-enum",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
