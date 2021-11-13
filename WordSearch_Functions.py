"""
########################################################################################################################
# SUB-FUNCTIONS NEEDED FOR RUNNING THE WORD SEARCH PROGRAM
# Author:           Angus Berg
# Date Created:     12/11/2021
########################################################################################################################
"""
from typing import List, Tuple

"""
###################################################################################
FUNCTION TO FIND INSTANCES OF A WORD IN A STRING
"""
def findWordsInString(word: str, source: str) -> List[Tuple[int, int]]:
    #Initialise the tracking index and output list
    currentStart: int = 0
    outputList: List[Tuple[int, int]] = []

    #Iterate along the string finding all instances of the word until reaching the end of the string or an error occurs
    while currentStart < len(source):
        try:
            currentIndex: int = source.index(word, currentStart)
            outputList.append((currentIndex, currentIndex + len(word)))
            currentStart = outputList[-1][1]
        except ValueError:
            break

    #Return the list of indexes
    return outputList