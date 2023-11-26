from classes.analysis_data import AnalysisData
from collections import defaultdict

class RadonData(AnalysisData):
    def __init__(self):
      self.average_file_score = 0
      self.average_code_block_type_scores = defaultdict(int)
      self.code_block_type_occurences = defaultdict(int)
      self.number_of_python_programs = 0
    def update_linter_data(self,linter_data):
      # total items = total number occurences in terms of files
        
        if "overall_score" in linter_data:
            self.average_file_score += linter_data["overall_score"] 
            self.number_of_python_programs += 1
        if "function_complexity" in linter_data:
            self.code_block_type_occurences["function"] += 1
            self.average_code_block_type_scores["function"] += linter_data["function_complexity"]
        if "class_complexity" in linter_data:
            self.code_block_type_occurences["class"] += 1
            self.average_code_block_type_scores["class"] += linter_data["class_complexity"]
        if "method_complexity" in linter_data:
            self.code_block_type_occurences["method"] += 1
            self.average_code_block_type_scores["method"] += linter_data["method_complexity"]
      
    def __update_average_code_block_type_scores(self):
        for code_block_type, score in self.average_code_block_type_scores.items():
            self.average_code_block_type_scores[code_block_type] = score / self.code_block_type_occurences[code_block_type]
    def __update_average_file_score(self):
        if self.number_of_python_programs > 0:
          self.average_file_score = self.average_file_score / self.number_of_python_programs
        else:
          self.average_file_score = None

    def to_dict(self):
        self.__update_average_code_block_type_scores()
        self.__update_average_file_score()
        return {
            "average_file_score": self.average_file_score,
            "average_code_block_type_scores": dict(self.average_code_block_type_scores)
        }
