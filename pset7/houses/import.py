from csv import reader, DictReader
from sys import argv
from cs50 import SQL

# open database in sql as db
db = SQL("sqlite:///students.db")

# check for length of command line arguments
if len(argv)!=2:
    print("usage error")
    exit()

# open csv file and read each row
with open(argv[1],"r") as characters:
    reader=reader(characters)
# 1st row will be name 2nd house and 3rd birth
    for row in reader:
        fullnamelist=row[0].split()
        first=fullnamelist[0]
        # store in string the name to parse it
        if len(fullnamelist)==3:
            middle=fullnamelist[1]
            last=fullnamelist[2]
            db.execute("INSERT INTO students(first,middle,last,house,birth) VALUES(?,?,?,?,?)",first,middle,last,row[1],row[2])
        elif len(fullnamelist)==2:
            last=fullnamelist[1]
            db.execute("INSERT INTO students(first,middle,last,house,birth) VALUES(?,?,?,?,?)",first,None,last,row[1],row[2])
