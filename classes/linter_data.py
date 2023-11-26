from collections import defaultdict
from classes.default_data import DefaultLinterData
from classes.radon_data import RadonData
from classes.violation_data import ViolationData
# Class to store linter data
class LinterData:
    # Class to store linter data
    def __init__(self, linter_name):
        # Create a ViolationData object to store the overall data
        if linter_name.lower() =="radon":
          self.overall = RadonData()
          self.by_tag = defaultdict(lambda: RadonData())
        elif linter_name.lower() == "black":
          self.overall = DefaultLinterData()
          self.by_tag = defaultdict(lambda: DefaultLinterData())
        else:
          self.overall = ViolationData()
        # Create a dictionary to store the data for each tag
          self.by_tag = defaultdict(lambda: ViolationData())
   # Function to convert the data to a dictionary
    def to_dict(self):
        return {
            "overall": self.overall.to_dict(),
            "by_tag": {tag: data.to_dict() for tag, data in self.by_tag.items()}
        }