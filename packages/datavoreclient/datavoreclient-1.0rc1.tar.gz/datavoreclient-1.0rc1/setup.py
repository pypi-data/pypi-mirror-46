from distutils.core import setup

with open("README.txt", "r") as fh:
    long_description = fh.read()

setup(
  name='datavoreclient',
  version='1.0rc1',
  url='http://www.ifremer.fr/datavore',
  py_modules=['datavoreclient'],
  packages=['datavoreclient'],
  author='LOPS Datavore team',
  author_email='lops-support-cloud@listes.ifremer.fr',
#   package_dir={'datavoreclient': 'datavoreclient'},
  description="Datavore-client - Python Client library to get data from LOPS Datavore services",
  classifiers=[
    "Programming Language :: Python",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  long_description=long_description,
  package_data={'datavoreclient': ['_build/html/index.html']},
  #data_files=[('test', ['test.py', 'test_2.py'])]
)
