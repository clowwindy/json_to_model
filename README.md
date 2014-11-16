JSON to model
=============

[![Build Status]][Travis CI]
[![PyPI version]][PyPI]

Convert JSON api to Objective-C and Swift model source files.

Got tired of writing models and JSON parsers? Then generate them automatically!

Please consider contributing code. Please send me bug reports and issues.

usage
-----

Suppose you have a json file `input/comment.json`:

```json
{
    "__class__": "User",
    "username": "Alice",
    "age": 17,
    "email": "alice@somemail.com",
    "registered": true
}
```

Run:

    pip install json_to_model
    json_to_model -i input/ -o output/

You'll get:

    ~/models/User.h
    ~/models/User.m

All properties and init methods and helper methods for JSON convertion
are also generated. `null` is handled. Other classes on the properties,
arrays will also be converted recursively.

See [tests] for how it works.


[Build Status]:      https://travis-ci.org/clowwindy/json_to_model.svg?branch=master
[PyPI]:              https://pypi.python.org/pypi/json_to_model
[PyPI version]:      https://img.shields.io/pypi/v/json_to_model.svg?style=flat
[Travis CI]:         https://travis-ci.org/clowwindy/json_to_model
[tests]:             https://github.com/clowwindy/json_to_model/tree/master/tests
