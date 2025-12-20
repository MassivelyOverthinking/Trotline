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
    def url(self) -> str:
        return self.data["url"]
    
    @property
    def status(self) -> bool:
        return self.data["status"]

    @property
    def is_https(self) -> bool:
        return self.data["is_https"]
    
    @property
    def domain_entropy(self) -> float:
        return self.data["domain_entropy"]
    
    @property
    def whois_registered(self) -> bool:
        registration = self.data["days_since_whois_reg"]
        return (registration is not None and registration != 0)
    
    @property
    def typosquatted(self) -> bool:
        return self.data["is_typosquatted"]
    
    def to_dict(self):
        return self.data
    
    def to_pandas(self):
        return pd.Series(self.data)
    
    def to_numpy(self):
        return np.ndarray(self.data)