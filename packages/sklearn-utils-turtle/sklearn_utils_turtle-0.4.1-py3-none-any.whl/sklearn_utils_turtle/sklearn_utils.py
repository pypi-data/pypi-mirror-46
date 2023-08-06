from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class ItemsSelector(BaseEstimator, TransformerMixin):
    """Extract features from each document for DictVectorizer"""
    def __init__(self, columns=None):
        self.columns = columns

    def fit(self, x, y=None):
        return self

    def transform(self, X):
        return X[self.columns]
    
    
class CategoricalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        self.columns = columns
        self.encoders = {key: dict() for key in self.columns}
    
    def fit(self, X, y=None):
        for col in self.columns:
            series = X[col]
            thisdict = self.encoders[col]
            i = 1
            for item in series:
                if item not in thisdict:
                    thisdict[item] = i
                    i += 1
        return self
    
    def transform(self, X):
        data = {}
        for col in self.columns:
            print
            items = []
            series = X[col]
            thisdict = self.encoders[col]
            for item in series:
                i = thisdict.get(item, 0)
                items.append(i)
            
            data[col] = items
        
        return pd.DataFrame(data=data)