# PyJsonAssert

This project aims to be a library for facilitating REST API testing.

[![Build Status](https://travis-ci.org/javierseixas/pyJsonAssert.svg?branch=master)](https://travis-ci.org/javierseixas/pyJsonAssert)
[![Coverage Status](https://coveralls.io/repos/github/javierseixas/pyJsonAssert/badge.svg?branch=master)](https://coveralls.io/github/javierseixas/pyJsonAssert?branch=master)

## Reason to be

I've been trying to find a library for testing APIs in python, which in my point of view requires to compare expected jsons with given jsons, as libraries like [PHP Matcher](https://github.com/coduo/php-matcher) or [JSONassert](https://github.com/skyscreamer/JSONassert) do.
My impossibility to find a library with these features, encourage me to do my own.

## Functionality

```python
from pyjsonassert import assert_json

expected = {"animal": "dog"}
current = {"animal": "cat"}

# Will fail
assert_json(expected, current)
```

You can also use some flags for strict comparison:

```python
from pyjsonassert import assert_json

expected = {"animal": "dog", "place": "home"}
current = {"animal": "dog", "object": "table"}

# Will assert
assert_json(expected, current, allow_unexpected_fields=True, allow_missing_fields=False)
```

## Running tests
```
python -m unittest discover tests
```


## Building the package
Build the distributions:
```
python setup.py sdist bdist_wheel
```
Upload to pypi:
```
twine upload dist/*
```
Upload to test.pypi:
```
twine upload -r test dist/*
```

## Release new version

This packages has configured an CI delivery flow using travis. For publishing new releases correctly in travis, it will be necessary to tag the release appropriately.

**NOTICE**: Remember to update the version manually in the `pyjsonassert/__init__.py` file.

## TODO
* Fix conflict with travis: jobs per version and deploy to pypi. After first success deploy, the other fail because dist is already uploaded.
* Add custom message parameter in the assertion
* Enable patterns for being able to match types, besides the exact value (like [PHP Matcher patterns](https://github.com/coduo/php-matcher#available-patterns))