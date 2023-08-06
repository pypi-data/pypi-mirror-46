
# `humanizer` [![PyPI version](https://badge.fury.io/py/humanizer.svg)](https://badge.fury.io/py/humanizer) [![Build Status](https://travis-ci.com/grimen/python-humanizer.svg?branch=master)](https://travis-ci.com/grimen/python-humanizer) [![Coverage Status](https://codecov.io/gh/grimen/python-humanizer/branch/master/graph/badge.svg)](https://codecov.io/gh/grimen/python-humanizer)

*A developer friendly data/value humanizer for debugging/logging - for Python.*


## Introduction

*TODO*


## Install

Install using **pip**:

```sh
$ pip install humanizer
```


## Use

Very basic **[example](https://github.com/grimen/python-humanizer/tree/master/examples/basic.py)**:

```python
from humanizer import bytesize, duration

# TODO: add example

```


## Test

Clone down source code:

```sh
$ make install
```

Run **colorful tests**, with only native environment (dependency sandboxing up to you):

```sh
$ make test
```

Run **less colorful tests**, with **multi-environment** (using **tox**):

```sh
$ make test-tox
```


## About

This project was mainly initiated - in lack of solid existing alternatives - to be used at our work at **[Markable.ai](https://markable.ai)** to have common code conventions between various programming environments where **Python** (research, CV, AI) is heavily used.


## License

Released under the MIT license.
