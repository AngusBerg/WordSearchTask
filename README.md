# WordSearchTask
Project produced in response to the word search task, provided by Solar Analytics.

This word search project is designed to read a word search grid and list of search words from a text file
(or any alternative file format that can be read as a text file, such as CSV, config or undefined extensions)
and then run the word search that has been extracted to find the search words in the grid, writing the results to file.

## Word Search Project Input
The input for this project needs to be a text file containing a grid of characters to be searched within at the top
of the file followed by at least one blank line and then the list of words that the program should try to find in the
grid; each of these search words needs to be on a new line.

In order to be considered valid, the input file has to have a searchable grid that is at least 1 line long, with all
the lines containing the same number of characters, and at least 1 word that will be searched for. As such, the minimal
valid input file would be three lines long; A single-line "grid" to be searched in at the top of the file, followed by a
blank break-line and then one word to be searched for within the single-line "grid". While a standard word search grid
is square, there is no requirement for the input grid to be square, only that every line of the grid is the same length.

### Note on character types
Please note that while a normal word-search would contain only alphabetic characters, this search will allow you to
search for any kind of character; It is just as able to search for words as it is for numbers, characters or any
combination of them.

## Word Search Project Output
This project outputs a text file containing the list of words that were found in the grid, followed by the X and Y
coordinates of the start and end positions of the word. Each of these output lines has the format
**"WORD (START-X, START-Y) (END-X, END-Y)"**.

The data is written out to a file in the same directory as the input file with the same name, but with its input file
extension replaced with the file extension ".out". If a file of that name and with the out extension already exists in
target folder, an underscore and a number will be appended to the file name to ensure that this process isn't
overwriting information that already exists.

## Running the Word Search Project
The Word Search Project is designed to be run from the command line. In order to be run properly, the command run must
contain at least the name of the main word search file followed by the name of the input file that is to be processed.
An example of what this command would look like is shown below; This command assumes you are executing the command line
from the folder containing both the word search python files and the input file.

> python WordSearch.py InputPuzzleFile.pzl

This project will allow you to run multiple input files at the same time, although this is not the best way to run this
script as an error in one of the early files will cancel the run of all following files. If run in this way, the command
to be run from the command line would look like the below example.

> python WordSearch.py InputPuzzleFile1.pzl InputPuzzleFile2.pzl InputPuzzleFile3.pzl InputPuzzleFile4.pzl ...

By default, the output file for this project will only hold one entry for each word that is being searched for. If you
would instead like to have the output files contain all the extracts for each word that is being searched for, you can
optionally provide a second argument of **"True"** to have the process write every instance of the words found to the
output file. If you wish to call the project like this, you would use a command like the one shown below.

> python WordSearch.py InputPuzzleFile.pzl True
