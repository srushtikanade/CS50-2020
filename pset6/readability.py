import math
import cs50

text = input("text:\n")
letters = 0
words = 1
sent = 0
for i in text:
    if i.isalpha():
        letters=letters+1
    if i.isspace():
        words=words+1
    if i == '.' or i == '!' or i == '?':
        sent=sent+1



g = round (0.0588 * ((100 * letters) / words) - 0.296 * ((100 * sent) / words) - 15.8)

if g >= 1 and g <=16:
    print(f"Grade {g}")
elif g<1:
    print("Before Grade 1")
elif g>16:
    print("Grade 16+")
