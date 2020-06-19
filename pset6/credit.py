digit1=0
digit2=0
cardlength=0
first_two_digits=0
sum_of_even=0
sum_of_double_odds=0
cardnum=int(input("enter your card number:\n"))

while cardnum>0:
    digit2=digit1
    digit1=cardnum%10

    if cardlength % 2==0:
        sum_of_even +=digit1
    else:
        multiple= 2*digit1
        sum_of_double_odds +=(multiple//10)+(multiple%10)

    cardnum//=10
    cardlength+=1

is_valid= (sum_of_even + sum_of_double_odds)%10==0
first_two_digits=(digit1*10)+digit2

if cardlength==15 and first_two_digits==34 or first_two_digits==37 and is_valid:
    print("AMEX")
elif cardlength==16 and first_two_digits >= 51 and first_two_digits <= 55 and is_valid:
    print("MASTERCARD")
elif cardlength==13  or cardlength==16 and digit1==4 and is_valid :
    print("VISA")
else:
    print("INVALID")
