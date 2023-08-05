from setuptools import setup

with open('README.md', 'r') as f:
  long_description = f.read()

setup(
  name='hellodude',
  version='0.0.2',
  description='Say hello dude',
  py_modules=["hellodude"],
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/bla",
  author="FooBar",
  author_email="Foo@Bar.Car",
  package_dir={'': 'src'},
  classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Operating System :: OS Independent",
      ]
)
