"""
########################################################################################################################
# SUB-FUNCTIONS NEEDED FOR RUNNING THE WORD SEARCH PROGRAM
# Author:           Angus Berg
# Date Created:     12/11/2021
########################################################################################################################
"""
from pathlib import Path
from typing import List, Tuple, Dict
from WordSearch_Classes import WordSearchResult, WordSearch

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

"""
########################################################################################################################
FUNCTION TO FIND ALL THE INSTANCES OF A WORD ON ALL LINES AND RETURN THE LIST OF RESULTS
- word: The word that will be searched for in the lines
- horizontalLines: The set of horizontal lines that will be searched for instances of the word
- verticalLines: The set of vertical lines that will be searched for instances of the word
"""
def extractInstancesAcrossAllLines(word: str, horizontalLines: List[str], verticalLines: List[str]) \
        -> List[WordSearchResult]:
    #Get the results for the horizontal lines
    extractionResults: List[WordSearchResult] = []
    for index, line in enumerate(horizontalLines):
        extractionResults.extend(extractAllInstancesInLine(word, line, index, False))

    #Get the results for the vertical lines
    for index, line in enumerate(verticalLines):
        extractionResults.extend(extractAllInstancesInLine(word, line, index, True))

    #Return the full list of results that have been extracted
    return extractionResults

"""
########################################################################################################################
FUNCTION TO EXTRACT ALL WORDS FROM A LOADED WORD SEARCH
- wordSearch: The word search information that has been parsed out of the input file
"""
def runLoadedWordSearch(wordSearch: WordSearch) -> Dict[str, List[WordSearchResult]]:
    #Declare the empty output dictionary
    outputDict: Dict[str, List[WordSearchResult]] = dict()

    #Perform the extraction for each of the words in the word-search. Add the entries as a new part of the dictionary
    for searchWord in wordSearch.words:
        results: List[WordSearchResult] = \
            extractInstancesAcrossAllLines(searchWord, wordSearch.horizontalLines, wordSearch.verticalLines)

        outputDict[searchWord] = results

    #Return the dictionary with the relevant entries
    return outputDict

"""
########################################################################################################################
FUNCTION TO WRITE THE RESULTS OF OF THE WORD SEARCH PROCESS TO FILE
"""
def writeTheResultsToFile(wordList: List[str], outputPath: str, results: Dict[str, List[WordSearchResult]]):
    #Run through the words in the list, adding their results to the output content string
    outputContent: str = ""

    for word in wordList:
        #Pull the content if it exists and convert to the output string
        try:
            currentResult = results[word][0].createOutputLine(1)
        except (KeyError, IndexError):
            currentResult = word.upper() + " not found"

        #Add the entry to the output string
        outputContent += currentResult + "\n"

    #Check that the output path doesn't lead to a pre-existing file
    if Path(outputPath).is_file():
        #Add an offset to ensure that the file path isn't filled
        count: int = 1

        while True:
            pathParts: List[str] = outputPath.split(".")
            offsetPath: str = ".".join(pathParts[:-1]) + "_" + str(count) + "." + pathParts[-1]

            #See if the offset path is unique. If not, increment the count and loop
            if Path(offsetPath).is_file():
                count += 1
            else:
                outputPath = offsetPath
                break

    #Write the information out to file
    with open(outputPath, "w") as file:
        file.write(outputContent)

    #Return from writing to file
    return
















