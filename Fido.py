name = input('Enter file name:')
fh = open(name)
mylist = list()
n = 0
for line in fh:
    line = line.split()
    for words in line:
        if words not in mylist:
            mylist.append(words)
            n  = n + 1 
if n > 1 :
    x = 2*n//3 + 1
    print(mylist[x])
else: print("Null")