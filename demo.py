data = [
    [1,2,3],
    [3,2,1],
    [4,3,4]
]

import csv

f = open('222.csv','w')
writer = csv.writer(f)
for i in data:
    writer.writerow(i)
f.close()