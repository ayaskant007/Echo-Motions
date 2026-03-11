f = open("file.txt")

lines = f.readlines()
# line1= f.readline()
# line2= f.readline()
print(lines)
line = f.readline()

while line!="":
    print(line)
    line = f.readline()

# print(line1, type(line1))
# print(line2, type(line2))
f.close()