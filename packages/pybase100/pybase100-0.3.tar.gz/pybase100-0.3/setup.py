import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='pybase100',
      version='0.3',
      description='A Python version of Base100 encoding mechanism',
      url='https://github.com/MasterGroosha/pybase100',
      author='Evgeny Petrov',
      author_email='groosha@protonmail.com',
      license='The Unlicence',
      packages=setuptools.find_packages(),
      zip_safe=False
)
