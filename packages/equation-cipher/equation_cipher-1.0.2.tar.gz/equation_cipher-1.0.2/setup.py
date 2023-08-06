import setuptools


# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
     name='equation_cipher',
     version='1.0.2',
     author="Shounak Joshi",
     author_email="shounakjoshi16@gmail.com",
     description="An Encryption algorithm for encrypting any text.",
     long_description='For the usage and feature description please refer'
                      ' to this link: https://equation-cipher.readthedocs.io/en/latest/index.html',
     long_description_content_type="text/markdown",
     url="https://github.com/malhar-stories/equation_cipher",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
