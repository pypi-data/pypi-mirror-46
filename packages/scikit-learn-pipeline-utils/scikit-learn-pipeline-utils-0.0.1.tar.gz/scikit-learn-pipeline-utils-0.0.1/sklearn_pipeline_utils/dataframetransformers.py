from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import Imputer, LabelEncoder, OneHotEncoder, OrdinalEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
import pandas as pd

class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.attribute_names].values.reshape(-1,1)

class DFObjectSelector(BaseEstimator, TransformerMixin):
    def __init__(self, _type):
        self.type = _type
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_type = X.select_dtypes(include=[self.type])
        X_type_columns = X_type.columns
        return pd.DataFrame(X_type, columns=X_type_columns, index=X.index)
    
class DFFeatureUnion(TransformerMixin):
    # FeatureUnion but for pandas DataFrames

    def __init__(self, transformer_list):
        self.transformer_list = transformer_list

    def fit(self, X, y=None):
        for (name, t) in self.transformer_list:
            t.fit(X, y)
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        Xts = [t.transform(X) for _, t in self.transformer_list]
        Xunion = reduce(lambda X1, X2: pd.merge(X1, X2, left_index=True, right_index=True), Xts)
        return Xunion
    
class DFImputer(TransformerMixin):
    # Imputer but for pandas DataFrames

    def __init__(self, strategy='mean'):
        self.strategy = strategy
        self.imp = None
        self.statistics_ = None

    def fit(self, X, y=None):
        self.imp = SimpleImputer(strategy=self.strategy)
        self.imp.fit(X)
        self.statistics_ = pd.Series(self.imp.statistics_, index=X.columns)
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        Ximp = self.imp.transform(X)
        Xfilled = pd.DataFrame(Ximp, index=X.index, columns=X.columns)
        return Xfilled
    
class DFImputerMostFrequent(TransformerMixin):
    
    def __init__(self):
        self.most_frequent = None
        
    def fit(self, X, y=None):
        self.most_frequent = pd.Series([X[c].value_counts().index[0] for c in X], index = X.columns)
        return self
    
    def transform(self, X, y=None):
        return X.fillna(self.most_frequent)
    
class DFOrdinalEncoder:
    def __init__(self):
        self.ordinal_encoder = None
        
    def fit(self, X, y = None):
        self.ordinal_encoder = OrdinalEncoder()
        self.ordinal_encoder.fit(X)
        return self
    
    def transform(self, X, y=None):
        t = self.ordinal_encoder.transform(X)
        return pd.DataFrame(t, columns=X.columns, index=X.index)
    
class DFStandardScaler:
    def __init__(self):
        self.standard_scaler = None
        
    def fit(self, X, y = None):
        self.standard_scaler = StandardScaler()
        self.standard_scaler.fit(X)
        return self
    
    def transform(self, X, y = None):
        t = self.standard_scaler.transform(X)
        return pd.DataFrame(t, columns = X.columns, index = X.index)

    
class DFMinMaxScaler:
    def __init__(self):
        self.minmax_scaler = None
        
    def fit(self, X, y = None):
        self.minmax_scaler = MinMaxScaler()
        self.minmax_scaler.fit(X)
        return self
    
    def transform(self, X, y = None):
        t = self.minmax_scaler.transform(X)
        return pd.DataFrame(t, columns = X.columns, index = X.index)