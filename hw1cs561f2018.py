from collections import Counter
import itertools


inputfile = open("input.txt")
n = int(inputfile.readline())
p = int(inputfile.readline())
scooter = int(inputfile.readline())

timestamp = []

rows = inputfile.readlines()

for row in rows:
    timestamp.append(row.strip())

timestamp = Counter(timestamp)

inputfile.close()

board = [-1] * n

track = []
all_solutions= []

def findMax(timestamp,polposition):
    maximum = -1
    for var1 in polposition:
        total = 0
        for var2 in var1:
            tmp01 = var2[0]
            tmp02 = var2[1]
            for time in timestamp.keys():
                tmptime = time.split(",")
                if int(tmptime[0]) == tmp01 and int(tmptime[1]) == tmp02:
                    total += timestamp[time]
        if total > maximum:
            maximum = total
    return maximum


def search(board,current,size,track,all_solutions,p,tmp):

    if p == 0:
        all_solutions.append(track[:])
        return

    for i in range(size):
        board[tmp[current]] = i
        if isSafe(board,current,tmp):
            track.append([tmp[current],i])
            search(board,current+1,size,track,all_solutions,p-1,tmp)
            board[tmp[current]] = -1
            track.pop()
    return

def isSafe(board,current,tmp):
    for i in range(current):
        if board[tmp[i]] == board[tmp[current]]:
            return False
        if tmp[current] - tmp[i] == abs(board[tmp[current]] - board[tmp[i]]):
            return False
    return True


a = list(itertools.combinations(range(n), n-p))



for tmp2 in a:
    tmp01 = range(n)
    for x in tmp2:
        if x in tmp01:
            tmp01.remove(x)
    search(board,0,n,track,all_solutions,p,tmp01)

maximum = str(findMax(timestamp,all_solutions))

outputfile = open("output.txt","w+")
outputfile.write(maximum)
outputfile.close()

