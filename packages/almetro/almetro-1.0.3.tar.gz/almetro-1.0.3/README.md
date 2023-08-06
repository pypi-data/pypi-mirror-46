Almetro Library
===============================

version number: 0.0.1
author: Arnour Sabino

Overview
--------

A python library to measure algorithms execution time and compare with its theoretical complexity.

[![Build Status](https://travis-ci.org/arnour/almetro.svg?branch=master)](https://travis-ci.org/arnour/almetro)

Installation / Usage
--------------------

To install use pip:

    $ pip install almetro


Or clone the repo:

    $ git clone https://github.com/arnour/almetro.git
    $ python setup.py install

Examples
--------------------

Applying Almetro to a quadratic algorithm:

```python
import almetro
from almetro.algorithms import loop_n_quadratic
from almetro.complexity import cn_quadratic
from almetro.instance import growing

metro = almetro\
            .new()\
            .with_execution(trials=5)\
            .with_instances(instances=20, provider=growing(initial_size=100, growth_size=100))\
            .metro(algorithm=loop_n_quadratic, complexity=cn_quadratic)

chart = metro.chart()

chart.show()
```

![Chart Almetro n quadratic](images/chart_almetro_n_quadratic.png)

---

Applying Almetro to a lg n algorithm:

```python
import almetro
from almetro.algorithms import loop_n_log
from almetro.complexity import clog_n
from almetro.instance import growing

metro = almetro\
            .new()\
            .with_execution(trials=100)\
            .with_instances(instances=20, provider=growing(initial_size=10000, growth_size=10000))\
            .metro(algorithm=loop_n_log, complexity=clog_n)

chart = metro.chart()

chart.show()
```

![Chart Almetro lg n](images/chart_almetro_lg_n.png)
