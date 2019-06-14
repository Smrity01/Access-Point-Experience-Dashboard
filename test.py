import csv
fd = open('review.csv','r')
writer = csv.reader(fd,delimiter = ',')
next(writer)
for row in writer:
    print(row)