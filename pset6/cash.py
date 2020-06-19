from cs50 import get_float
from math import floor

while True:
    dollars_owed=get_float("change owed:\n")
    cents_owed=floor(dollars_owed*100)
    if cents_owed>0.00:
        break

quarters = cents_owed // 25
dimes = (cents_owed % 25) // 10
nickels = ((cents_owed % 25) % 10) // 5
pennies = ((cents_owed % 25) % 10) % 5

print(f"{quarters + dimes + nickels + pennies}")
