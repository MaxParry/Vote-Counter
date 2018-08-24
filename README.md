![Poll Image](images/Vote_counting.jpg)

# Vote-Counter
Simple python script to ingest ballot CSVs of different formats, parse data, and determine election winner.

## Problem
Two reporting counties have submitted .csv files containing poll results for counting and analysis. The data is in the same format for both files. The goal of the project will be to tally the votes, and determine a winner for the state.

## Data Structure
The .csv files are arranged with three columns:
* Voter ID (integer)
* County (string)
* Candidate (string)

## Strategy
The only pertinent column for the analysis (assuming nobody voted twice!) will be the candidate column.

No transformation of the data is necessary, only iterating over rows to count the number of times each candidate is listed, along with a count of total number of votes. With these numbers in hand, we will be able to calculate the percentage of total votes for each candidate, and determine a winner.

## Script
### Exploration
In order to view the structure of the data and determine what the header rows look like, the function `shown(n)` was written to print n rows of a .csv to the console.

A few things to note about this function:
* It uses the `os` module's `path.join()` function in order to piece together the source directory and filename, in order to use the appropriate directory seperator for the OS being used by the user.
* The `open()` function is used inside a `with` statement to ensure the file is closed after reading.
* The `csv` module allows for easy reading of csvs, by allowing construction of a `reader` object, an iterable with rows of the csv as elements. Columns of these elements are accessed with list slicing.
* A counter is initialized in the outer loop, and incremented in the inner loop, in order to keep count of rows. The inner loop checks this counter against the supplied argument in order to break the loop after n rows.

The data showed one header row per file, a typical .csv structure. Looking at the header rows in each file using this function, they are identical.

### Counting Total Votes
In order to compare each candidate's vote count to a total of all votes cast, it was necessary to total all votes. The function `countvotes()` was written to accomplish this.

A few things to note about this function:
* It is constructed much like `shown()`, with an outer loop iterating over files, and an inner loop iterating through rows in those files with `csv` module's `reader()` function.
* There are two counters in the loop, one initialized and incremented in the outer loop, and another in the inner loop. The inner loop counter serves to count rows in an individual file, and the outer loop counter `totcount` keeps track of counts for all files.
* Because the first column of the header row is always `'Voter ID'`, it provided an easy way to skip that row during vote counting. (Line 55)

### Listing Unique Candidates
In order to store tallies of each candidate's votes, we first needed a list of unique candidates. `listcand()` performs that function, and returns this list.

A few things to note about this function:
* An empty list to hold unique candidates is initialized at the beginning of the function
* It is structured similarly to `countvotes()`, iterating over csv files, then rows in the csv, skipping headers.
    * The difference is that for each row, the function checks if the candidate listed in the row is already in the candidate list. If not, the candidate is added.

### Tallying Votes
Now that we have a list of unique candidates, the strategy was as follows:
* Initialize a dictionary of the structure `{"Candidate":[percentage, votes]}` using the list of unique candidates
    * Placeholder integers `[0,0]` were used to initialize
* Iterate over files, then rows in file as before, each time comparing the candidate listed in the vote to each candidate in the dictionary
    * Keep count of the total number of rows (votes) iterated over
    * When a match is found, update the dictionary to increment the votes for the corresponding candidate
        * Also update the percentage of candidate votes to total votes in the dictionary for the corresponding candidate.

The function `tallyvotes()` performs this operation. A few notes about this function:
* It constructs a candidate dictionary as described above by using a for loop to iterate over the list of unique candidates, each time creating a new entry in the initialized `candidatedict`
* It is structured similarly to `countvotes()`, except when a row is iterated over:
    * Each key in the `candidatedict` is compared to the candidate column of the row being iterated over until a match is found (line 118), whereupon vote count and percentage of current total votes is recalculated.

### Finding the Winner
After the dictionary of candidates, their vote counts, and their percentage of total votes was constructed, it was easy to iterate over it to find the winner. The function `findwinner()` accomplishes this in the following way:
* A comparison variable, `topdog`, is initialized as 0
* `.items()` accessor is used to iterate over key, value pairs in the `candidatedict`
* Percentage of total votes for a candidate is read and compared with `topdog`. If it is larger, it is stored as the new `topdog`, and the corresponding candidate is stored as `winner`.

### Running Functions
Each of the above functions, except for `shown()`, is run in succession, and the returned data stored as a variable. Now that the data has been aggregated, it is time to print the results.

### Printing and Writing to File
`printresults()` prints results of the vote count to the console.

`printsep()` is a helper function used to write newlines in-between results to make the .txt file more readable.

The `printtofile()` function uses `os` module's `path.join()` function in tandem with `open()` to open a blank .txt file to write the election results with the help of `printsep()` by iterating over the `candidatedict` and printing the variables captured in lines 144-147.

`printresults()` and `printtofile()` are run at the end of the script.