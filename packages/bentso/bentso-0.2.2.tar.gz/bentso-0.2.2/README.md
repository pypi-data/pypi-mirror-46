# bentso

A library to process ENTSO-E electricity data for use in industrial ecology and life cycle assessment. Developed as part of the [BONSAI](https://bonsai.uno/) network.

[![Travis CI Status](https://travis-ci.org/BONSAMURAIS/bentso.svg?branch=master)](https://travis-ci.org/BONSAMURAIS/bentso) [![Appveyor CI status](https://ci.appveyor.com/api/projects/status/2fol87o7el4humq9?svg=true)](https://ci.appveyor.com/project/cmutel/bentso) [![Coverage Status](https://coveralls.io/repos/github/BONSAMURAIS/bentso/badge.svg?branch=master)](https://coveralls.io/github/BONSAMURAIS/bentso?branch=master) [![Documentation Status](https://readthedocs.org/projects/bentso/badge/?version=latest)](https://bentso.readthedocs.io/en/latest/?badge=latest)

See the [documentation](https://bentso.readthedocs.io/en/latest/) for more.

## Example living life cycle inventory model

Living life cycle inventory models can:

* Automatically update themselves
* Provide results on multiple spatial scales
* Provide results on multiple time scales

This particular model is quite simple - we will gather the necessary data from the [ENTSO-E API](https://github.com/BONSAMURAIS/hackathon-2019),
and return it in the specified RDF format. The model should support the following capabilities:

* Be able to specify what kind of input parameters it accepts
* Validate inputs and return sensible error messages
* Cache data to avoid unncessary ENTSO-E API calls
* Function both as a command-line utility and a normal Python library

Inputs can be a list of countries (default is all countries in ENTSO-E), and a time period (default is a given year - maybe 2018?).

This model should also follow the [BONSAI Python library skeleton](https://github.com/BONSAMURAIS/python-skeleton).
