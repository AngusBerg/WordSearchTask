"""
########################################################################################################################
# CUSTOM CLASSES USED BY THE WORD SEARCH PROGRAM
# Author:           Angus Berg
# Date Created:     12/11/2021
########################################################################################################################
"""
from typing import Tuple

"""
#######################################################################
# CLASS TO HOLD THE RESULTS OF A WORD FOUND IN THE WORD SEARCH
#######################################################################
"""
class WordSearchResult:
    #Initialisation function for the results class
    def __init__(self, word: str, startPosition: Tuple[int, int], endPosition: Tuple[int, int]):
        self.word: str = word
        self.startX: int = startPosition[0]
        self.startY: int = startPosition[1]
        self.endX: int = endPosition[0]
        self.endY: int = endPosition[1]

    #Function to convert the contents of the results class into the output line for the results file
    def createOutputLine(self, offset: int = 0) -> str:
        startPart = "(" + str(self.startX + offset) + ", " + str(self.startX + offset) + ")"
        endPart = "(" + str(self.endX + offset) + ", " + str(self.endY + offset) + ")"
        return self.word + " " + startPart + " " + endPart