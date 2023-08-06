MASS (Mueen's Algorithm for Similarity Search)
----------------------------------------------

[<img src="https://img.shields.io/pypi/v/mass_ts.svg">](https://pypi.python.org/pypi/mass_ts)
[<img src="https://img.shields.io/travis/tylerwmarrs/mass-ts.svg">](https://travis-ci.org/tylerwmarrs/mass-ts)
[<img src="https://readthedocs.org/projects/mass-ts/badge/?version=latest">](https://mass-ts.readthedocs.io/en/latest/?badge=latest)

MASS is the fundamental algorithm that the matrix profile algorithm is built on top of. It allows you to search a time series for a smaller series. The result is an array of distances. To find the "closest" section of a time series to yours, simply find the minimum distance(s).

mass-ts is a python 2 and 3 compatible library.

* Free software: Apache Software License 2.0


Features
--------

* MASS - the first implementation of MASS
* MASS2 - the second implementation of MASS that is significantly faster. Typically this is the one you will use.
* MASS3 - a piecewise version of MASS2 that can be tuned to your hardware. Generally this is used to search very large time series.
* MASS2_batch - a batch version of MASS2 that reduces overall memory usage, provides parallelization and enables you to find top K number of matches within the time series. The goal of using this implementation is for very large time series similarity search.

Installation
------------
```
pip install mass-ts
```

Example Usage
-------------
A dedicated repository for practical examples can be found at the [mass-ts-examples repository](https://github.com/tylerwmarrs/mass-ts-examples).

```python

import numpy as np
import mass_ts as mts

ts = np.loadtxt('ts.txt')
query = np.loadtxt('query.txt')

# mass
distances = mts.mass(ts, query)

# mass2
distances = mts.mass2(ts, query)

# mass3
distances = mts.mass3(ts, query, 256)

# mass2_batch
# start a multi-threaded batch job with all cpu cores and give me the top 5 matches.
# note that batch_size partitions your time series into a subsequence similarity search.
# even for large time series in single threaded mode, this is much more memory efficient than
# MASS2 on its own.
batch_size = 10000
top_matches = 5
n_jobs = -1
indices, distances = mts.mass2_batch(ts, query, batch_size, 
    top_matches=top_matches, n_jobs=n_jobs)

# find minimum distance
min_idx = np.argmin(distances)
```

Citations
---------
Abdullah Mueen, Yan Zhu, Michael Yeh, Kaveh Kamgar, Krishnamurthy Viswanathan, Chetan Kumar Gupta and Eamonn Keogh (2015), The Fastest Similarity Search Algorithm for Time Series Subsequences under Euclidean Distance, URL: http://www.cs.unm.edu/~mueen/FastestSimilaritySearch.html
