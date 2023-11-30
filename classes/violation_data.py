from collections import defaultdict
from classes.default_data import DefaultLinterData
from constants import constants
class ViolationData(DefaultLinterData):
  # Class to store violation data
    def __init__(self):
      super().__init__()
      self.average_violations_per_line = 0
    # Function to update the violation data
    def update_linter_data(self, linter_data):
      self.total_violations += linter_data[constants.TOTAL_VIOLATIONS_KEY]
      
      self.number_of_python_programs += 1
      self.average_violations_per_line += (linter_data[constants.TOTAL_VIOLATIONS_KEY] / linter_data[constants.NUMBER_OF_LINES_IN_CODE_KEY]) 
      self._update_violation_frequencies(linter_data)
    def __update_average_violations_per_line(self):
      if self.number_of_python_programs > 0:
        self.average_violations_per_line = self.average_violations_per_line / self.number_of_python_programs
      else:
        self.average_violations_per_line = None
    # Function to convert the data to a dictionary
    def to_dict(self):
        self._update_most_frequent_violation()
        self._update_top_violations()
        self._update_average_violations_per_file()
        self.__update_average_violations_per_line()
        # Return the data as a dictionary
        return {
            constants.TOTAL_VIOLATIONS_KEY: self.total_violations,
            constants.VIOLATION_DATA_AVERAGE_VIOLATIONS_PER_LINE_KEY: self.average_violations_per_line,
            constants.VIOLATION_DATA_AVERAGE_VIOLATIONS_PER_FILE_KEY: self.average_violations_per_file,
            constants.VIOLATION_DATA_VIOLATION_FREQUENCIES_KEY: dict(self.violation_frequencies),
            constants.VIOLATION_DATA_MOST_FREQUENT_VIOLATION_KEY: self.most_frequent_violation,
            constants.VIOLATION_DATA_TOP_VIOLATIONS_KEY: self.top_violations
        }
