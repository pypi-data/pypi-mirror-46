# QuantX SDK for Python

A Python library for the QuantX API.

## Installation


    pip install QuantX-SDK

## Usage

Initialize.

```python
from quantx_sdk import QX
qx = QX(public_key, secret_key)
```

You can get projects.

```python
>>> qx.projects()
[
  {
    "name": "project name".
    "hash": "xxx"
  },
  ...
]
```

You can get source code.

```python
>>> project = qx.projects()[0]
>>> project.source()
source code...
```

You can upload source code

```python
>>> project.upload_source("source code")
>>> # or
>>> project.upload_source_file("hoge.py")
```

You can run backtest

```python
>>> backtest = project.backtest({'engine': 'maron-0.0.1b', 'to_date': '2017-12-31', 'from_date': '2017-12-01', 'capital_base': 10000000})
>>> # or
>>> backtest = project.backtest({}) # run default backtest parameters
>>> result = backtest.join() # backtest running other thread.
>>> summary = result.summary() # get backtest sumamry
>>> benchmark = result.benchmark() # benchmark is DataFrame
```
