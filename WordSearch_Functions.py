"""
########################################################################################################################
# SUB-FUNCTIONS NEEDED FOR RUNNING THE WORD SEARCH PROGRAM
# Author:           Angus Berg
# Date Created:     12/11/2021
########################################################################################################################
"""
from typing import List, Tuple
from WordSearch_Classes import WordSearchResult

"""
########################################################################################################################
FUNCTION TO FIND INSTANCES OF A WORD IN A STRING
- word: The word to be found in the source string
- source: The source string that will be search
"""
def findWordsInString(word: str, source: str) -> List[Tuple[int, int]]:
    #Initialise the tracking index and output list
    currentStart: int = 0
    outputList: List[Tuple[int, int]] = []

    #Iterate along the string finding all instances of the word until reaching the end of the string or an error occurs
    while currentStart < len(source):
        try:
            currentIndex: int = source.index(word, currentStart)
            outputList.append((currentIndex, currentIndex + len(word) - 1))
            currentStart = outputList[-1][1] + 1
        except ValueError:
            break

    #Return the list of indexes
    return outputList

"""
########################################################################################################################
FUNCTION TO FIND FORWARD AND BACKWARD INSTANCES OF A WORD IN A LONGER STRING AND RETURN A LIST OF THE RESULTS CLASS
- word: The word to be found in the source string
- line: The full line of the word search that is being examined
- lineNum: The index of the line that is being examined
- vertical: A boolean telling the function whether or not the line being examined is vertical. False means horizontal
"""
def extractAllInstancesInLine(word: str, line: str, lineNum: int, vertical: bool = False) -> List[WordSearchResult]:
    #Convert the word and line to all lower-case
    lowerWord: str = word.lower()
    lowerLine: str = line.lower()

    #Extract all instances of the word in the line, both forwards and backwards
    forwardResults: List[Tuple[int, int]] = findWordsInString(lowerWord, lowerLine)
    backwardResults: List[Tuple[int, int]] = findWordsInString(lowerWord[::-1], lowerLine)

    #Reverse the backward result order and append the results together, unless the word is a palindrome
    if lowerWord in lowerWord[::-1]:
        searchResults: List[Tuple[int, int]] = forwardResults
    else:
        searchResults: List[Tuple[int, int]] = [(ff[1], ff[0]) for ff in backwardResults]
        searchResults.extend(forwardResults)

    #Branch based on if this line is vertical or horizontal and construct the results
    if vertical:
        return [WordSearchResult(lowerWord.capitalize(), (lineNum, yy[0]), (lineNum, yy[1])) for yy in searchResults]
    else:
        return [WordSearchResult(lowerWord.capitalize(), (xx[0], lineNum), (xx[1], lineNum)) for xx in searchResults]