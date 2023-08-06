# uprime
[![by Dashlane](./by_dashlane.svg)](https://www.dashlane.com/)

A python implementation the u'-chart.  

The u'-chart is a control chart for attributes data that can handle large and variable sample sizes by counteracting overdispersion as described in the following paper: David B. Laney (2002) Improved Control Charts for Attributes, Quality Engineering, 14:4, 531-537, DOI: 10.1081/QEN-120003555.

The u'-chart is used to evaluate an attribute statistic over a period of time to determine whether or not the variation in the statistic can be explained by random variation alone.

This module includes customizable options that facilitates its use as an alerting system.

Author: Robert Astel

**TL;DR**: Implementation of u'-prime control chart rules that can be used for creating alerts on statistics with high/variable sample sizes.

## Get Started

### Install 
~~~~
pip install uprime
~~~~

### Usage
```python
from uprime import Uprime

# Four required arguments:
  # 1. Pandas Dataframe
  # 2. Name of the column by which the data can be chronologically sorted
  # 3. Name of the column that contains the number of occurrences of the attribute of interest
  #    The number of occurrences should always be an integer.  Non-integer values will be rounded.
  # 4. Name of the column that contains the size of the subgroup (A.K.A. sample)
  #    The subgroup size should always be an integer.  Non-integer values will be rounded.
up = Uprime(df, 'sort_column_name', 'occurrences_column_name', 'subgroup_size_column_name')

# Perform u'-chart calculations
# Return a Pandas DataFrame that contains all necessary data to plot a u'-chart or trigger alerts 
up_df = up.frame()
```


## Examples
`method = rolling, periods = 30`

This configuration performs u'-chart calculations using the previous rolling 30 periods for each subgroup.

This is different from the default `method = 'all'`, which uses all subgroups in the DataFrame df to perform the calculations`.

```python
up = Uprime(df, 'sort_column_name', 'occurrences_column_name', 'subgroup_size_column_name', 
            method = 'rolling', periods = 30)
```

More [examples](./examples), including usage of other optional arguments and built in charting function.


## Contributing

Read our [CONTRIBUTING.md](./CONTRIBUTING.md) to learn about our development process.

## License

uprime is licensed under the  [Apache License 2.0](./LICENSE)
