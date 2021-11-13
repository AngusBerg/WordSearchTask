"""
########################################################################################################################
# UNIT TESTS FOR THE WORD SEARCH FUNCTIONS
# Author:           Angus Berg
# Date Created:     12/11/2021
########################################################################################################################
"""
import pytest
from typing import List
import WordSearch_Functions as wsFunc
from WordSearch_Classes import WordSearchResult

"""
#######################################################################################
# FIND WORDS IN STRING FUNCTION TESTS
#######################################################################################
"""
class TestFindWordsInString:
    #Test that the function can find a word in itself
    def test_matchString(self):
        testResult = wsFunc.findWordsInString("match", "match")
        assert (len(testResult) == 1 and testResult[0][0] == 0 and testResult[0][1] == 4)

    #Test that the function can find a word in a longer string
    def test_findString(self):
        testResult = wsFunc.findWordsInString("find", "the word find is in this string")
        assert (len(testResult) == 1 and testResult[0][0] == 9 and testResult[0][1] == 12)

    #Test that the function returns multiple results when a string is repeated in the input
    def test_repeatedString(self):
        testResult = wsFunc.findWordsInString("repeat", "repeat repeat repeat")
        assert (len(testResult) == 3 and testResult[0][0] == 0 and testResult[2][0] == 14)

    #Test that the function returns an empty string if the word is not present
    def test_stringNotFound(self):
        testResult = wsFunc.findWordsInString("found", "the chosen word is not in this string")
        assert len(testResult) == 0

"""
#######################################################################################
# FIND ALL INSTANCES IN A LINE AND CONSTRUCT OUTPUT FUNCTION TESTS
#######################################################################################
"""
class TestExtractAllInstancesInLine:
    #Test that the function will construct an instance correctly out of a simple forwards match
    def test_extractExactString(self):
        testResult: WordSearchResult = wsFunc.extractAllInstancesInLine("match", "match", 0, False)[0]
        assert (testResult.startX == 0 and testResult.endX == 4)

    #Test that the function will construct an instance correctly when looking for a vertical match
    def test_extractVerticalExactString(self):
        testResult: WordSearchResult = wsFunc.extractAllInstancesInLine("match", "match", 0, True)[0]
        assert (testResult.startY == 0 and testResult.endY == 4)

    #Test that the function will construct an instance correctly out of a simple backwards match
    def test_extractReversedExactString(self):
        testResult: WordSearchResult = wsFunc.extractAllInstancesInLine("match", "hctam", 0, False)[0]
        assert (testResult.startX == 4 and testResult.endX == 0)

    #Test that the function will extract both forwards and backwards instances of the word from the line
    def test_extractRepeatedWords(self):
        testLine: str = "wordworddrowwordrow"
        testResults: List[WordSearchResult] = wsFunc.extractAllInstancesInLine("word", testLine, 0, False)
        uniqueResults: List[int] = list(set([rr.startX for rr in testResults]))

        assert (len(testResults) == 5 and len(uniqueResults) == 5)

    #Test that the function will correctly find instances of a word regardless of capitalisation
    def test_caseInsensitiveExtract(self):
        testResult: List[WordSearchResult] = wsFunc.extractAllInstancesInLine("test", "testTESTtEsT", 0, False)
        assert len(testResult) == 3

    #Test that the function does not return duplicate results when the word it is looking for is a palindrome
    def test_palindromesArentRepeated(self):
        testResult: List[WordSearchResult] = wsFunc.extractAllInstancesInLine("hannah", "hannahhannah", 0, False)
        assert len(testResult) == 2

    #Test that the function will return an empty list when there are no matches for the word
    def test_noMatchesInLine(self):
        testResult: List[WordSearchResult] = wsFunc.extractAllInstancesInLine("unmatched", "<>?@#&!^#*!#)(", 0, False)
        assert len(testResult) == 0

























