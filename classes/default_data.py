from collections import defaultdict

from classes.analysis_data import AnalysisData
from constants.constants import FREQUENCY_KEY
from constants.constants import VIOLATION_DATA_VIOLATION_FREQUENCIES_KEY
from constants.constants import VIOLATION_DATA_MOST_FREQUENT_VIOLATION_KEY
from constants.constants import VIOLATION_DATA_TOP_VIOLATIONS_KEY
from constants.constants import VIOLATION_DATA_AVERAGE_VIOLATIONS_PER_FILE_KEY
from constants.constants import TOTAL_VIOLATIONS_KEY
from constants.constants import VIOLATION_TYPE_KEY
from constants.constants import VIOLATIONS_KEY
class DefaultLinterData(AnalysisData):
  # Class to store violation data
    def __init__(self):
      self.total_violations = 0
      self.average_violations_per_file = 0
      self.most_frequent_violation = {FREQUENCY_KEY: 0, VIOLATION_TYPE_KEY: ""}
      self.violation_frequencies = defaultdict(int)
      self.top_violations = []
      self.number_of_python_programs = 0
    # Function to update the violation data
    def update_linter_data(self, linter_data):
      self.total_violations += linter_data[TOTAL_VIOLATIONS_KEY]
      self.number_of_python_programs += 1
      self._update_violation_frequencies(linter_data)
    
    def _update_average_violations_per_file(self):
      if self.number_of_python_programs > 0:
        self.average_violations_per_file = self.total_violations / self.number_of_python_programs
      else:
        self.average_violations_per_file = None
    def _update_violation_frequencies(self, linter_data):
      for violation_type, violation_count in linter_data[VIOLATIONS_KEY].items():
        self.violation_frequencies[violation_type] += violation_count 
    # Function to update the most frequent violation
    def _update_most_frequent_violation(self):
        for violation_type, count in self.violation_frequencies.items():
            if count > self.most_frequent_violation[FREQUENCY_KEY]:
                self.most_frequent_violation = {FREQUENCY_KEY: count, VIOLATION_TYPE_KEY: violation_type}
    # Function to update the top three violations
    def _update_top_violations(self):
        # Sort the violation frequencies and pick the top three
        sorted_violations = sorted(self.violation_frequencies.items(), key=lambda item: item[1], reverse=True)
        self.top_violations = sorted_violations[:3]
    # Function to convert the data to a dictionary
    def to_dict(self):
        self._update_most_frequent_violation()
        self._update_top_violations()
        self._update_average_violations_per_file()
        # Return the data as a dictionary
        return {
            TOTAL_VIOLATIONS_KEY: self.total_violations,
            VIOLATION_DATA_AVERAGE_VIOLATIONS_PER_FILE_KEY: self.average_violations_per_file,
            VIOLATION_DATA_VIOLATION_FREQUENCIES_KEY: dict(self.violation_frequencies),
            VIOLATION_DATA_MOST_FREQUENT_VIOLATION_KEY: self.most_frequent_violation,
            VIOLATION_DATA_TOP_VIOLATIONS_KEY: self.top_violations
        }
