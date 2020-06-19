from sys import argv
from cs50 import SQL

# check for length of command line arguments
if len(argv)!=2:
    print("usage error")
    exit()

# open database
db = SQL("sqlite:///students.db")
# perfrom query and save the return value/result in studentslist
studentslist = db.execute("SELECT * FROM students WHERE house = (?) ORDER BY last", argv[1])

# for each row in the list
for student in studentslist:
    if student["middle"] != None:
        print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")
    else:
        print(f"{student['first']} {student['last']}, born {student['birth']}")
