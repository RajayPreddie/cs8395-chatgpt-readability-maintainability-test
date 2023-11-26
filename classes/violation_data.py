from collections import defaultdict
from classes.default_data import DefaultLinterData
class ViolationData(DefaultLinterData):
  # Class to store violation data
    def __init__(self):
      super().__init__()
      self.average_violations_per_line = 0
    # Function to update the violation data
    def update_linter_data(self, linter_data):
      self.total_violations += linter_data["total_violations"]
      
      self.number_of_python_programs += 1
      self.average_violations_per_line += (linter_data["total_violations"] / linter_data["number_of_lines_in_code"]) 
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
            "total_violations": self.total_violations,
            "average_violations_per_line": self.average_violations_per_line,
            "average_violations_per_file": self.average_violations_per_file,
            "violation_frequencies": dict(self.violation_frequencies),
            "most_frequent_violation": self.most_frequent_violation,
            "top_violations": self.top_violations
        }
