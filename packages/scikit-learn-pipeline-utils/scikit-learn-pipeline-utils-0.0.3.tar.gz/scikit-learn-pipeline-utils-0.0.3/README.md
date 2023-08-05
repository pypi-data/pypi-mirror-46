# Helpful Package For Custom Transformers To Use In Sklearn Pipelines

## Installation
`pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple scikit-learn-pipeline-utils`

## Quick Start
```
from sklearn_pipeline_utils import DFSelector
from sklearn.pipeline import Pipeline
import pandas as pd

df = pd.DataFrame({
    "col1": ["a", "b", "a"],
    "col2": [1, 2, 3]
})

pipeline = Pipeline([
    ("dfselectcol1", DFSelector("col1"))
    ])

print(pipeline.transform(df))
'''
expected result:
  col1
0    a
1    b
2    a
'''
```

## Dataframe Transformers List
1. DFSelector
2. DFObjectSelector
3. DFFeatureUnion
4. DFImputer
5. DFImputerMostFrequent
6. DFOrdinalEncoder
7. DFStandardScaler 