import os
import csv

# identify location of source data
sourcedirectory = 'input_data'
file1 = 'election_data_1.csv'
file2 = 'election_data_2.csv'

# wrap files in list for iteration
filelist = [file1, file2]


# for exploration, shown(n) prints n number of rows in each file

def shown(n):
    # iterate over files
    for afile in filelist:
        # initialize row counter
        counter = 0
        # construct filepath using appropriate directory seperators
        path = os.path.join(sourcedirectory, afile)
        # open file to read, use with statement so file closes afterward
        with open(path, 'r', newline='') as f:
            # create reader object (iterable with .csv rows as elements)
            reader = csv.reader(f)
            # iterate over rows in .csv
            for row in reader:
                # increment row counter
                counter = counter + 1
                # print current row
                print(row)
                # stop printing rows when row counter == supplied argument
                if counter >= n:
                    break


# countvotes() returns total number of votes, skipping headers

def countvotes():
    # initialize vote counter
    totcount = 0
    # iterate over .csv files
    for afile in filelist:
        # initialize counter for all files
        counter = 0
        # construct filepath using appropriate directory seperators
        path = os.path.join(sourcedirectory, afile)
        # open file to read, use with statement so file closes afterward
        with open(path, 'r', newline='') as f:
            # create reader object (iterable with .csv rows as elements)
            reader = csv.reader(f)
            # iterate over rows in .csv
            for row in reader:
                # pass row if it is a header, typified by 'Voter ID'
                if row[0] == 'Voter ID':
                    pass
                # if not a header row, increment single file row counter
                else:
                    counter = counter + 1
        # when finished counting rows in file, add to counter for all files
        totcount = totcount + counter
    return totcount

# listcand() returns a list of unique candidates

def listcand():
    # create list to hold unique candidates
    candidates = []
    # iterate over .csv files
    for afile in filelist:
        # construct filepath using appropriate directory seperators
        path = os.path.join(sourcedirectory, afile)
        # open file to read, use with statement so file closes afterward
        with open(path, 'r', newline='') as f:
            # create reader object (iterable with .csv rows as elements)
            reader = csv.reader(f)
            # iterate over rows in .csv
            for row in reader:
                # skip header row
                if row[0] == 'Voter ID':
                    pass
                else:
                    # check to see if current candidate is in list
                    if row[2] not in candidates:
                        # if new candidate, add to candidate list
                        candidates.append(row[2])
                    else:
                        pass
    return candidates 

# tallyvotes() returns a dictionary: {"Candidate":[percentage, votes]}

def tallyvotes():
    # initialize dictionary
    candidatedict = {}
    # iterate over list of unique candidates
    for candidate in candidates:
        # initialize list of 2 integers for each candidate key
        candidatedict[candidate] = [0,0]

    # iterate over poll files
    for afile in filelist:
        # create filepath with appropriate directory seperators
        path = os.path.join(sourcedirectory, afile)
        # open file to read
        with open(path, 'r', newline='') as f:
            # create reader object to iterate over rows in .csv
            reader = csv.reader(f)
            # iterate over rows
            for row in reader:
                # skip headers
                if row[0] == 'Voter ID':
                    pass
                else:
                    # iterate over initialized candidate dictionary
                    for key, value in candidatedict.items():
                        # when candidate dictionary key matches voter candidate
                        if key == row[2]:
                            # increment vote value (2nd element in dict value list)
                            value[1] = value[1] + 1
                            # update percent votes for candidate in dict
                            value[0] = round(((value[1] / totcount) * 100), 1)
                        else:
                            pass
    return candidatedict

# findwinner() returns key (candidate name string) of highest vote count value               

def findwinner():
    # initialize comparison value
    topdog = 0
    # iterate over each unique candidate in dict
    for key, value in candidatedict.items():
        # if largest vote count so far, store as top vote count
        if value[1] > topdog:
            topdog = value[1]
            # store corresponding candidate name
            winner = key
        else:
            pass
    return winner

# run above functions in sequence
totcount = countvotes()
candidates = listcand()
candidatedict = tallyvotes()
winner = findwinner()

# function for easy line seperator in .txt output
def printsep():
    print('\n', ('-' * 30))

# printresults() formats .txt file output
def printresults():

    print('Election Results')
    printsep()
    print('\n', 'Total Votes:', totcount)
    printsep()
    # print contents of candidate dictionary with % formatting
    for key, value in candidatedict.items():
        print('\n' + key + ':', str(value[0]) + '%  (' + str(value[1]) + ')')
    printsep()
    print('\n' + 'Winner: ', winner)
    printsep()

# printtofile() opens output file to write and writes results of analysis
def printtofile():
    path = os.path.join('output_data', 'election_results.txt')
    with open(path, 'w', newline='') as f:
        f.write('Election Results')
        f.write('\n' + ('-' * 30))
        f.write('\n' + 'Total Votes: ' + str(totcount))
        f.write('\n' + ('-' * 30))
        for key, value in candidatedict.items():
            f.write('\n' + key + ': ' + str(value[0]) + '%  (' + str(value[1]) + ')')
        f.write('\n' + ('-' * 30))
        f.write('\n' + 'Winner: ' + winner)
        f.write('\n' + ('-' * 30))

# execute above functions to record election result
printresults()
printtofile()