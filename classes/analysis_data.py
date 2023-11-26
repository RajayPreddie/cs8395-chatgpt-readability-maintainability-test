from abc import ABC, abstractmethod


class AnalysisData(ABC):
    def __init__(self):
      pass
        

    @abstractmethod
    def update_linter_data(self, linter_data):
        pass


    @abstractmethod
    def to_dict(self):
        pass
