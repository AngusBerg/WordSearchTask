"""
########################################################################################################################
# SUB-FUNCTIONS NEEDED FOR RUNNING THE WORD SEARCH PROGRAM
# Author:           Angus Berg
# Date Created:     12/11/2021
########################################################################################################################
"""
import os
from pathlib import Path
from typing import List, Tuple, Dict
from WordSearch_Classes import WordSearchResult, WordSearch

"""
########################################################################################################################
FUNCTION TO FIND INSTANCES OF A WORD IN A STRING
"""
def findWordsInString(word: str, source: str) -> List[Tuple[int, int]]:
    """
    FUNCTION TO FIND INSTANCES OF A WORD IN A STRING

    :param word: The word to be found in the source string
    :param source: The source string that will be search
    :return: A list of "(start, end)" index tuples showing where in the source the word was found
    """

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
"""
def extractAllInstancesInLine(word: str, line: str, lineNum: int, vertical: bool = False) -> List[WordSearchResult]:
    """
    FUNCTION TO FIND FORWARD AND BACKWARD INSTANCES OF A WORD IN A LONGER STRING

    :param word: The word to be found in the source string
    :param line: The full line of the word search that is being examined
    :param lineNum: The index of the line that is being examined
    :param vertical: A boolean telling the function whether or not the line being examined is vertical.
                     False means that the line is a horizontal row.
    :return: A list of the "WordSearchResults" class containing every instance of the word that was found.
    """

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
        return [WordSearchResult(lowerWord.upper(), (lineNum, yy[0]), (lineNum, yy[1])) for yy in searchResults]
    else:
        return [WordSearchResult(lowerWord.upper(), (xx[0], lineNum), (xx[1], lineNum)) for xx in searchResults]

"""
########################################################################################################################
FUNCTION TO FIND ALL THE INSTANCES OF A WORD ON ALL LINES AND RETURN THE LIST OF RESULTS
"""
def extractInstancesAcrossAllLines(word: str, horizontalLines: List[str], verticalLines: List[str]) \
        -> List[WordSearchResult]:
    """
    FUNCTION TO FIND ALL THE INSTANCES OF A WORD ON ALL LINES AND RETURN THE LIST OF RESULTS

    :param word: The word that will be searched for in the lines
    :param horizontalLines: The set of horizontal lines that will be searched for instances of the word
    :param verticalLines: The set of vertical lines that will be searched for instances of the word
    :return: A list of the "WordSearchResults" class containing every instance of the word that was found.
    """

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
"""
def runLoadedWordSearch(wordSearch: WordSearch) -> Dict[str, List[WordSearchResult]]:
    """
    FUNCTION TO EXTRACT ALL WORDS FROM A LOADED WORD SEARCH

    :param wordSearch: The word search information that has been loaded into the required class
    :return: A dictionary, keyed by the words that were searched for in the grid and containing each of their list of
             "WordSearchResult" objects.
    """

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
FUNCTION TO DETERMINE WHAT THE OUTPUT FILE PATH SHOULD BE BASED ON THE INPUT FILE PATH
"""
def determineOutputPath(inputPath: str) -> str:
    """
    FUNCTION TO DETERMINE WHAT THE OUTPUT FILE PATH SHOULD BE BASED ON THE INPUT FILE PATH

    :param inputPath: The input file path for this project run
    :return: A valid but currently unused output file path in the same directory as the input
    """

    #Determine which character is being used to split directories in the current file system
    breakChar: str = "\\" if "\\" in os.getcwd() else "/"

    #Pull the target folder and file name out of the input path
    pathParts: List[str] = inputPath.split(breakChar)
    dirParts: List[str] = pathParts[:-1]
    inputFile: str = pathParts[-1]

    #Update the input file and append to the directory parts. Branch to account for files with no file type extension
    if "." in inputFile:
        dirParts.append(".".join(inputFile.split(".")[:-1]) + ".out")
    else:
        dirParts.append(inputFile + ".out")

    #Join the path parts together
    outputPath: str = breakChar.join(dirParts)

    #Check that this file doesn't already exist. Append on an offset number if it does
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

    #Return the derived output path
    return outputPath

"""
########################################################################################################################
FUNCTION TO WRITE THE RESULTS OF OF THE WORD SEARCH PROCESS TO FILE
"""
def writeTheResultsToFile(wordList: List[str], outputPath: str, results: Dict[str, List[WordSearchResult]],
                          showAll: bool = False) -> str:
    """
    FUNCTION TO WRITE THE RESULTS OF OF THE WORD SEARCH PROCESS TO FILE

    :param wordList: The list of words that were searched for in the word search
    :param outputPath: The output path that the results are to be written to
    :param results: The word-keyed dictionary containing the results of the word search
    :param showAll: A boolean indicating whether the top result for each word or all the results for each word should
                    be written out to file.
    :return: A message string confirming that the results were written to file and the file path to which they were
             written.
    """

    #Run through the words in the list, adding their results to the output content string
    outputContent: str = ""

    for word in wordList:
        #Pull the content if it exists and convert to the output string.
        # - Offset of 1 applied so that the top corner is coded as (1,1) rather than the python standard of (0,0)
        try:
            if showAll and len(results[word]) > 0:
                currentResult = "\n".join([item.createOutputLine(1) for item in results[word]])
            elif showAll:
                currentResult = word.upper() + " not found"
            else:
                currentResult = results[word][0].createOutputLine(1)
        except (KeyError, IndexError):
            currentResult = word.upper() + " not found"

        #Add the entry to the output string
        outputContent += currentResult + "\n"

    #Write the information out to file
    with open(outputPath, "w") as file:
        file.write(outputContent)

    #Return from writing to file; Return a message with the output path infixed
    return "Results of word search written out. The output file is \"{}\"".format(outputPath)