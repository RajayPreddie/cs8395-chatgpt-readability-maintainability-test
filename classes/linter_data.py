from collections import defaultdict
from classes.default_data import DefaultLinterData
from classes.radon_data import RadonData
from classes.violation_data import ViolationData
from constants.linters import RADON, BLACK
from constants.constants import LINTER_DATA_BY_TAG_DATA_KEY, LINTER_DATA_OVERALL_DATA_KEY
# Class to store linter data
class LinterData:
    # Class to store linter data
    def __init__(self, linter_name):
        # Create a ViolationData object to store the overall data
        if linter_name.lower() ==RADON:
          self.overall = RadonData()
          self.by_tag = defaultdict(lambda: RadonData())
        elif linter_name.lower() == BLACK:
          self.overall = DefaultLinterData()
          self.by_tag = defaultdict(lambda: DefaultLinterData())
        else:
          self.overall = ViolationData()
        # Create a dictionary to store the data for each tag
          self.by_tag = defaultdict(lambda: ViolationData())
   # Function to convert the data to a dictionary
    def to_dict(self):
        return {
            LINTER_DATA_OVERALL_DATA_KEY: self.overall.to_dict(),
            LINTER_DATA_BY_TAG_DATA_KEY: {tag: data.to_dict() for tag, data in self.by_tag.items()}
        }