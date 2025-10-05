
from abc import ABC, abstractmethod
class DataPoint(dict): pass
class Adapter(ABC):
    def __init__(self, cfg): self.cfg = cfg
    @abstractmethod
    def fetch(self): ...
