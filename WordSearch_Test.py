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
from WordSearch_Classes import WordSearchResult, WordSearch, InvalidWordSearchFile

"""
#######################################################################################
# WORD SEARCH RESULTS CLASS TESTS
#######################################################################################
"""
class TestWordSearchResult:
    #Test that the output line generation function works correctly
    def test_outputLineGeneration(self):
        testResult: WordSearchResult = WordSearchResult("Test", (0, 0), (3, 3))
        testOutLine: str = testResult.createOutputLine()

        assert testOutLine in "Test (0, 0) (3, 3)"

    #Test that the offset argument of the output line generation works correctly
    def test_outputLineGenerationWithOffset(self):
        testResult: WordSearchResult = WordSearchResult("Test", (0, 0), (3, 3))
        testOutLine: str = testResult.createOutputLine(2)

        assert testOutLine in "Test (2, 2) (5, 5)"

"""
#######################################################################################
# WORD SEARCH CLASS TESTS
#######################################################################################
"""
class TestWordSearch:
    #Test that the function can correctly read the small test file
    def test_readSmallTestFile(self):
        testSearch: WordSearch = WordSearch("TestFiles/3x8_TestSearch.txt")

        correctWords: bool = (len(testSearch.words) == 2)
        correctHoris: bool = (len(testSearch.horizontalLines) == 3 and len(testSearch.horizontalLines[0]) == 8)
        correctVerts: bool = (len(testSearch.verticalLines) == 8 and len(testSearch.verticalLines[0]) == 3)

        assert (correctWords and correctHoris and correctVerts)

    #Test that the function can correctly read the larger test file
    def test_readLargeTestFile(self):
        testSearch: WordSearch = WordSearch("TestFiles/5x10_TestSearch.txt")

        correctWords: bool = (len(testSearch.words) == 5)
        correctHoris: bool = (len(testSearch.horizontalLines) == 5 and len(testSearch.horizontalLines[0]) == 10)
        correctVerts: bool = (len(testSearch.verticalLines) == 10 and len(testSearch.verticalLines[0]) == 5)

        assert (correctWords and correctHoris and correctVerts)

    #Test that the class throws the correct custom error when there is no content in the file
    def test_noContentInTestFile(self):
        with pytest.raises(InvalidWordSearchFile):
            WordSearch("TestFiles/NoContent_TestSearch.txt")

    #Test that the class throws the correct custom error when there are no words to look for in the file
    def test_noSearchableWordsInTestFile(self):
        with pytest.raises(InvalidWordSearchFile):
            WordSearch("TestFiles/NoWords_TestSearch.txt")

    #Test that the class throws the correct custom error when the lines of the Word Search are of different lengths
    def test_linesOfVariedLengthsInTestFile(self):
        with pytest.raises(InvalidWordSearchFile):
            WordSearch("TestFiles/VariedLengths_TestSearch.txt")

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

"""
#######################################################################################
# FIND ALL INSTANCES ACROSS GIVEN LINES FUNCTION TESTS
#######################################################################################
"""
class TestExtractInstancesAcrossAllLines:
    #Test that the function pulls can pull an instance from every line
    def test_simpleExtractAllLinesSimple(self):
        testLines: List[str] = ["match", "match", "match", "match", "match"]
        testResults: List[WordSearchResult] = wsFunc.extractInstancesAcrossAllLines("match", testLines, testLines)

        assert len(testResults) == (2 * len(testLines))

    #Test that the function pulls the correct number of instances when there are different numbers of results on lines
    def test_simpleExtractAllLinesMixed(self):
        testLines: List[str] = ["catcatdog", "dogdogcat", "catcatcat", "dogdogdog", "winnebago"]
        testResults: List[WordSearchResult] = wsFunc.extractInstancesAcrossAllLines("dog", testLines, testLines)

        assert len(testResults) == 12

    #Test that the function returns an empty list when there are no matching results
    def test_noInstancesOnAnyLine(self):
        testLines: List[str] = ["hello", "this", "is", "a", "unit", "test"]
        testResults: List[WordSearchResult] = wsFunc.extractInstancesAcrossAllLines("unfound", testLines, testLines)

        assert len(testResults) == 0

    #Test that the function runs correctly when no vertical lines are provided
    def test_noVerticalLinesProvided(self):
        testLines: List[str] = ["alphabet", "alphabet", "alphabet", "alphabet", "alphabet"]
        testResults: List[WordSearchResult] = wsFunc.extractInstancesAcrossAllLines("alpha", testLines, [])

        assert len(testResults) == 5

    #Test that the function runs correctly when no horizontal lines are provided
    def test_noHorizontalLinesProvided(self):
        testLines: List[str] = ["alphabet", "alphabet", "alphabet", "alphabet", "alphabet"]
        testResults: List[WordSearchResult] = wsFunc.extractInstancesAcrossAllLines("alpha", [], testLines)

        assert len(testResults) == 5

    #Test that the function runs correctly when no lines are provided at all
    def test_noLinesProvided(self):
        testResults: List[WordSearchResult] = wsFunc.extractInstancesAcrossAllLines("alpha", [], [])

        assert len(testResults) == 0























