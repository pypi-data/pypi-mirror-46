# AquaCropPy

Python port of AquaCrop code 

![matlab code structure](https://github.com/noah-de/AquaCropPy/blob/master/References/legacy-code-map.png)

## Building with tests included

This module was [built](https://docs.python.org/3.7/distutils/builtdist.html#creating-built-distributions) to be tested, released and installed like any other [python package](https://packaging.python.org/tutorials/packaging-projects/). Someday users will be able to *pip install* it from Pypi.

For now, developers will need to download the repo and instal it in '[editable mode](https://docs.pytest.org/en/latest/existingtestsuite.html#existingtestsuite)' to avoid having to re-build it:

    pip install -e .

### Running tests
Leveraging [pytest](https://docs.pytest.org/) with the pytest-cov module:

    pytest -v --cov=aquacroppy

Alternatively, you could run the unit tests with [nose](https://nose.readthedocs.io/en/latest/):

    nosetests  --with-coverage --cover-package=aquacroppy -v

### Test Driven Development
The idea is to only write code that meets a specification. Generally speaking, the specifications are the tests.

Here is a sample workflow:
  - start with a test suite that passes
  - write a test for code that does not yet exist
  - run the test, (confirm that it fails)
  - write the minimal amount of code to get the test to pass
  - run the entire test suite again (confirm that new code doesn't break other parts of the application)
  - commit code repository
  - repeat
  
### Building distribution
After checking out the repo, run the following command if you want to generate distributions:
    
    python3 setup.py sdist bdist_wheel
