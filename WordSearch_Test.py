"""
########################################################################################################################
# UNIT TESTS FOR THE WORD SEARCH FUNCTIONS
# Author:           Angus Berg
# Date Created:     12/11/2021
########################################################################################################################
"""
import pytest
import WordSearch_Functions as wsFunc

"""
#######################################################################################
# FIND WORDS IN STRING FUNCTION TESTS
#######################################################################################
"""
class TestFindWordsInString:
    #Test that the function can find a word in itself
    def test_matchString(self):
        testResult = wsFunc.findWordsInString("match", "match")
        assert (len(testResult) == 1 and testResult[0][0] == 0)

    #Test that the function can find a word in a longer string
    def test_findString(self):
        testResult = wsFunc.findWordsInString("find", "the word find is in this string")
        assert (len(testResult) == 1 and testResult[0][0] == 9)

    #Test that the function returns multiple results when a string is repeated in the input
    def test_repeatedString(self):
        testResult = wsFunc.findWordsInString("repeat", "repeat repeat repeat")
        assert (len(testResult) == 3 and testResult[0][0] == 0 and testResult[2][0] == 14)

    #Test that the function returns an empty string if the word is not present
    def test_stringNotFound(self):
        testResult = wsFunc.findWordsInString("found", "the chosen word is not in this string")
        assert len(testResult) == 0