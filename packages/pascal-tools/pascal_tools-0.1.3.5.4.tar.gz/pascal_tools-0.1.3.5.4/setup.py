from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()



setup(name='pascal_tools',
      version='0.1.3.5.4',
      description='Some useful tools for me ! ',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/moreaupascal56/pascal_tools',
      author='Pascal Moreau',
      author_email='moreaupascal56@gmail.com',
      license='free',
      packages=['pascal_tools'],
      zip_safe=False)