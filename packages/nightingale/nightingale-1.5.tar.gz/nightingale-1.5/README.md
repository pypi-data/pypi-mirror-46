# *Nightingale*

I named this package *Nightingale* in honour of 
[Florence Nightingale](https://en.wikipedia.org/wiki/Florence_Nightingale), 
[The lady with the data](https://thisisstatistics.org/florence-nightingale-the-lady-with-the-data/).

# Installation

You can use pip to install Nightingale:

```bash
pip install nightingale
```

# Usage

## Population Proportion

```python
from nightingale import get_sample_size, PopulationProportion, get_z_score

print('z-score for 0.95 confidence:', get_z_score(confidence=0.95))
print('sample size:', get_sample_size(confidence=0.95, error_margin=0.05, population_size=1000))
print('with 10% group proportion:', get_sample_size(confidence=0.95, error_margin=0.05, population_size=1000, group_proportion=0.1))

population_proportion = PopulationProportion(sample_n=239, group_proportion=0.5)
print('error:', population_proportion.get_error(confidence=0.95))
```

## Ordinary Least Squares (OLS)

```python
import pandas as pd
import numpy as np
from nightingale import OrdinaryLeastSquares

data = pd.DataFrame({
    'x': np.random.normal(size=20, scale=5), 
    'y': np.random.normal(size=20, scale=5),
})
data['z'] = data['x'].values + data['y'].values + np.random.normal(size=20, scale=1)
print('data:')
display(data.head())

ols = OrdinaryLeastSquares(data=data, formula='z ~ x + y')
print('ols results:')
display(ols.table)

print('r-squared:', ols.r_squared)
print('adjusted r-squared:', ols.adjusted_r_squared)

print('\n', 'summary:')
display(ols.summary)
```

## *ANOVA*


# References
z-score: https://stackoverflow.com/questions/20864847/probability-to-z-score-and-vice-versa-in-python

