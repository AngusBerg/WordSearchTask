"""
########################################################################################################################
# MAIN FILE FOR THE RUNNING OF THE WORD SEARCH PROJECT
# Author:           Angus Berg
# Date Created:     12/11/2021
########################################################################################################################
"""
import sys
from typing import List
from pathlib import Path
from WordSearch_Classes import WordSearch
from WordSearch_Functions import runLoadedWordSearch, writeTheResultsToFile

#Pull the system arguments as a global. Skip the first which is the script name
wordSearchPath: List[str] = sys.argv[1:]

"""
########################################################################################################################
MAIN FUNCTION FOR THE WORD SEARCH PROGRAM
"""
def wordSearchMain(inputPath: str, fullResultsFlag: bool = False):
    #Read the file information into a word search class
    wordSearchInfo: WordSearch = WordSearch(inputPath)

    #Run the word search function
    wordSearchResults = runLoadedWordSearch(wordSearchInfo)

    #Create the output file path
    outPath: str = ".".join(inputPath.split(".")[:-1]) + ".out"

    #Write the results to file, print the success message and return
    print(writeTheResultsToFile(wordSearchInfo.words, outPath, wordSearchResults, fullResultsFlag))
    return

#Run the process from here if this is the main
if __name__ == '__main__':
    #Run for every arg that is a valid input
    for index, strArg in enumerate(wordSearchPath):
        if Path(strArg).is_file():
            #Determine if the argument following the one being used is a boolean
            # - If true, the boolean indicates that full results should be output
            fullResults = False
            try:
                if "true" in wordSearchPath[index + 1].lower() and not Path(wordSearchPath[index + 1]).is_file():
                    fullResults = True
            except IndexError:
                pass

            #Run the program
            wordSearchMain(strArg, fullResults)