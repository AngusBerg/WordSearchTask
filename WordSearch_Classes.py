"""
########################################################################################################################
# CUSTOM CLASSES USED BY THE WORD SEARCH PROGRAM
# Author:           Angus Berg
# Date Created:     12/11/2021
########################################################################################################################
"""
from typing import Tuple, List

"""
#######################################################################
# CUSTOM EXCEPTION CLASS THROWN WHEN PARSING INVALID WORD SEARCHES
#######################################################################
"""
class InvalidWordSearchFile(Exception):
    pass

"""
#######################################################################
# CLASS TO HOLD THE RESULTS OF A WORD FOUND IN THE WORD SEARCH
#######################################################################
"""
class WordSearchResult:
    #Initialisation function for the results class
    def __init__(self, word: str, startPosition: Tuple[int, int], endPosition: Tuple[int, int]):
        """
        CLASS TO HOLD THE RESULT OF A SUCCESSFUL WORD SEARCH

        :param word: The word that is found between the provided coordinates
        :param startPosition: A tuple of ints containing the (X, Y) position of the first letter of the word
        :param endPosition: A tuple of ints containing the (X, Y) position of the last letter of the word
        """

        self.word: str = word
        self.startX: int = startPosition[0]
        self.startY: int = startPosition[1]
        self.endX: int = endPosition[0]
        self.endY: int = endPosition[1]

    #Function to convert the contents of the results class into the output line for the results file
    def createOutputLine(self, offset: int = 0) -> str:
        """
        METHOD TO GENERATE A LINE OF THE OUTPUT FROM THE WORD SEARCH RESULT IN THIS INSTANCE

        :param offset: An optional number by which to offset the coordinates
        :return: A string starting with the word and followed by the start and end coordinates in string
                 representations of tuples.
        """

        startPart = "(" + str(self.startX + offset) + ", " + str(self.startY + offset) + ")"
        endPart = "(" + str(self.endX + offset) + ", " + str(self.endY + offset) + ")"
        return self.word + " " + startPart + " " + endPart

"""
#######################################################################
# CLASS TO HOLD THE WORD SEARCH ITSELF. PARSES OUT FROM FILE
#######################################################################
"""
class WordSearch:
    #Initialisation function to build the word search from the input class
    def __init__(self, path: str):
        """
        CLASS TO HOLD A WORD SEARCH AS EXTRACTED FROM INPUT FILE

        :param path: The path to the text or text-like file that contains the word search
        """

        #Initialise the tracking variables
        breakLineFound: bool = False
        searchLines: List[str] = []
        searchWords: List[str] = []

        #Open the file at the path and read in the lines, segmenting them into the required categories
        with open(path, "r") as file:
            lines = file.readlines()

        for line in lines:
            #Drop the new line character from the line
            if len(line) == 0:
                lineWithoutBreak: str = line
            elif line[-1] in "\n":
                lineWithoutBreak: str = line[:-1]
            else:
                lineWithoutBreak: str = line

            #Branch to the correct handling of the line
            if len(lineWithoutBreak) == 0:
                #No content in line; If there is content in the search lines, the break-line has been found
                breakLineFound = (len(searchLines) > 0)
            elif breakLineFound:
                #If this line is after the break-line, it is a word for the search; append to the list
                searchWords.append(lineWithoutBreak)
            else:
                #If this line has content and is before the break-line, it is a line of the search; append to the list
                searchLines.append(lineWithoutBreak)

        #Check that for misformatting and raise an error if the file read in is invalid
        if len(searchLines) == 0:
            raise InvalidWordSearchFile("There was no content to be read from the provided input file")
        elif len(searchWords) == 0:
            raise InvalidWordSearchFile("No words could be found in the file after the Word Search Grid was extracted")
        elif len(set([len(line) for line in searchLines])) != 1:
            raise InvalidWordSearchFile("The lines of the Word Search Grid provided are not all the same length")

        #Declare the needed values for this class, creating the vertical lines by zipping the horizontal lines
        self.words: List[str] = searchWords
        self.horizontalLines: List[str] = searchLines
        self.verticalLines: List[str] = ["".join(list(zz)) for zz in zip(*searchLines)]