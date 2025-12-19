# ----------------------------------------
# IMPORTS
# ----------------------------------------

import json
import pandas as pd
import numpy as np

# ----------------------------------------
# PYPI MODELS
# ----------------------------------------

class TrotResult:

    __slots__ = ("data")

    def __init__(self, data):
        self.data: dict = json.loads(data)

    @property
    def url(self):
        return self.data["url"]
    
    @property
    def status(self):
        return self.data["status"]
    
    def to_dict(self):
        return self.data
    
    def to_pandas(self):
        return pd.Series(self.data)
    
    def to_numpy(self):
        return np.ndarray(self.data)