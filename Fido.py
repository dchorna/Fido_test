name = input('Enter file name:')
try:
  fh = open(name)
except FileNotFoundError:
    print("File with this name not found")
    exit()
mylist = list()
for line in fh:
    line = line.split()
    for words in line:
        if words not in mylist:
            mylist.append(words)
n = len(mylist)
if n > 1 :
    x = 2*n//3 - 1
    print(mylist[x])
else: print("Null")