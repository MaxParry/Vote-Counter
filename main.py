import os
import csv

sourcedirectory = 'input_data'
file1 = 'election_data_1.csv'
file2 = 'election_data_2.csv'
filelist = [file1, file2]


# for exploration, prints n number of rows in each file

def shown(n):
    for afile in filelist:
        counter = 0
        path = os.path.join(sourcedirectory, afile)
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                counter = counter + 1
                print(row)
                if counter >= n:
                    break


# countvotes() returns total number of votes, skipping headers

def countvotes():
    totcount = 0
    for afile in filelist:
        counter = 0
        path = os.path.join(sourcedirectory, afile)
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'Voter ID':
                    pass
                else:
                    counter = counter + 1
        totcount = totcount + counter
    return totcount

# listcand() returns a list of unique candidates

def listcand():
    candidates = []
    for afile in filelist:
        path = os.path.join(sourcedirectory, afile)
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'Voter ID':
                    pass
                else:
                    if row[2] not in candidates:
                        candidates.append(row[2])
                    else:
                        pass
    return candidates 

# tallyvotes() returns a dictionary: {"Candidate":[percentage, votes]}

def tallyvotes():

    candidatedict = {}
    for candidate in candidates:
        candidatedict[candidate] = [0,0]


    for afile in filelist:
        path = os.path.join(sourcedirectory, afile)
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'Voter ID':
                    pass
                else:
                    for key, value in candidatedict.items():
                        if key == row[2]:
                            value[1] = value[1] + 1
                            value[0] = round(((value[1] / totcount) * 100), 1)
                        else:
                            pass
    return candidatedict

# findwinner() returns key (candidate name string) of highest vote count value               

def findwinner():
    topdog = 0
    for key, value in candidatedict.items():
        if value[1] > topdog:
            topdog = value[1]
            winner = key
        else:
            pass
    return winner

totcount = countvotes()
candidates = listcand()
candidatedict = tallyvotes()
winner = findwinner()

def printsep():
    print('\n', ('-' * 30))

def printresults():

    print('Election Results')
    printsep()
    print('\n', 'Total Votes:', totcount)
    printsep()
    for key, value in candidatedict.items():
        print('\n' + key + ':', str(value[0]) + '%  (' + str(value[1]) + ')')
    printsep()
    print('\n' + 'Winner: ', winner)
    printsep()

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


printresults()
printtofile()