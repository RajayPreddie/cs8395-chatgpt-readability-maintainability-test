from classes.analysis_data import AnalysisData
from collections import defaultdict
from constants.constants import OVERALL_SCORE_KEY, CLASS_CODE_BLOCK_TYPE, METHOD_CODE_BLOCK_TYPE, FUNCTION_CODE_BLOCK_TYPE, RADON_AVERAGE_CODE_BLOCK_TYPE_SCORES_KEY, RADON_AVERAGE_FILE_SCORE_KEY
class RadonData(AnalysisData):
    def __init__(self):
      self.average_file_score = 0
      self.average_code_block_type_scores = defaultdict(int)
      self.code_block_type_occurences = defaultdict(int)
      self.number_of_python_programs = 0
    def update_linter_data(self,linter_data):
      # total items = total number occurences in terms of files
        
        if OVERALL_SCORE_KEY in linter_data:
            self.average_file_score += linter_data[OVERALL_SCORE_KEY] 
            self.number_of_python_programs += 1
        if FUNCTION_CODE_BLOCK_TYPE in linter_data:
            self.code_block_type_occurences[FUNCTION_CODE_BLOCK_TYPE] += 1
            self.average_code_block_type_scores[FUNCTION_CODE_BLOCK_TYPE] += linter_data[FUNCTION_CODE_BLOCK_TYPE]
        if CLASS_CODE_BLOCK_TYPE in linter_data:
            self.code_block_type_occurences[CLASS_CODE_BLOCK_TYPE] += 1
            self.average_code_block_type_scores[CLASS_CODE_BLOCK_TYPE] += linter_data[CLASS_CODE_BLOCK_TYPE]
        if METHOD_CODE_BLOCK_TYPE in linter_data:
            self.code_block_type_occurences[METHOD_CODE_BLOCK_TYPE] += 1
            self.average_code_block_type_scores[METHOD_CODE_BLOCK_TYPE] += linter_data[METHOD_CODE_BLOCK_TYPE]
      
    def __update_average_code_block_type_scores(self):
        for code_block_type, score in self.average_code_block_type_scores.items():
            self.average_code_block_type_scores[code_block_type] = score / self.code_block_type_occurences[code_block_type]
    def __update_average_file_score(self):
        if self.number_of_python_programs > 0:
          self.average_file_score = self.average_file_score / self.number_of_python_programs
        else:
          self.average_file_score = -1

    def to_dict(self):
        self.__update_average_code_block_type_scores()
        self.__update_average_file_score()
        return {
            RADON_AVERAGE_FILE_SCORE_KEY: self.average_file_score,
            RADON_AVERAGE_CODE_BLOCK_TYPE_SCORES_KEY: dict(self.average_code_block_type_scores)
        }
