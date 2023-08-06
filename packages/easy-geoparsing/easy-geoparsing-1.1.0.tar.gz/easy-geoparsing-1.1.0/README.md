easy-geoparsing
---

Easy-to-use module for streamlined parsing of countries from plaintext locations and top-level domains, plus manipulation of country names and ISO 2 & 3 character codes.

Implementation relies on:

- the [RESTcountries](https://restcountries.eu/) API
- the [geotext](https://pypi.org/project/geotext/) module

## installation

To install from the command line via [pip](https://pip.pypa.io/en/stable/), do:

`pip install easy-geoparsing`

To upgrade to the latest version via `pip` do:

`pip install easy-geoparsing --upgrade`

To use via [pipenv](https://docs.pipenv.org/en/latest/) put the following in your Pipfile:

```
[packages]
easy-geoparsing = ">=1.0.0"
```

## development

If you've cloned the repository, the best way to make it work is using `pipenv`

If you don't yet have `pipenv`, you can use `pip` to install it from the command line:

`pip install pipenv --upgrade`

Then, in the top level directory of this repository, `easy-geoparsing`, do:

`pipenv install --dev`

This will create the virtual environment and install the requirements (viewable in the Pipfile). The `--dev` flag will install packages needed for testing etc.

## usage

### GETTING STARTED

Do the following to get the parser utilities, noting that creating an instance of `EasyCountryParser` will automatically download the country data payload from RESTcountries and set up all the resources. Speed will therefore depend on your internet connection, but the payload is not large.

```
from easy_geoparsing import EasyCountryParser

ez_parser = EasyCountryParser()
```

or, if you don't want to use our alternative names for some of the countries (i.e. you want to exactly follow the RESTcountries standard)

`ez_parser = EasyCountryParser(altnames=False)`

The `EasyCountryParser` class provides utilities, based on the data from the RESTcountries API and the GeoText natural-language parser library, for easily extracting and handling country names and codes.

### PARSER RESOURCES

The parser is initialised with the following resources:

  - `.data`       - pandas DataFrame containing RESTcountries data
  - `.tld_to_a2c` - python dict, maps TLDs to 2-character ISO codes
  - `.tld_to_a3c` - python dict, maps TLDs to 3-character ISO codes
  - `.iso2to3`    - python dict, maps 2-character ISO codes to 3
  - `.iso3to2`    - python dict, maps 3-character ISO codes to 2
  - `.a2c_map`    - python dict, maps 2-char ISO codes to full names
  - `.a3c_map`    - python dict, maps 3-char ISO codes to full names

### PARSER METHODS

The parser has the following methods for handling locations data:

  - `.retrieve_country` - parses plaintext for extractable 2-character ISO codes for countries (which can then be manipulated using the mappers above)
