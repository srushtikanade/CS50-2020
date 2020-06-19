#include<stdio.h>
#include<cs50.h>

int main ()
{
int digit1=0;
int digit2=0;
int cardlength=0;
int first_two_digits=0;
int sum_of_even=0;
int sum_of_double_odds=0;
long long cardnum=get_long_long("enter your card number:\n");

//do it for the length of card, taking last number and finding if odd/even and updating those counters
while (cardnum>0)
{ // we store value of digit1 in digit2 to use for first_two_digits; digit2 will be second digit while digit1 after %10 will be first digit in last iteration

 digit2=digit1;
 digit1=cardnum%10;

  if(cardlength%2==0)
 {
    sum_of_even+=digit1; // += to update after each /10(next number)
 }
else
{
    int multiple=2*digit1;
sum_of_double_odds+=(multiple/10)+(multiple%10);  // += to update after each /10(next number)
}
cardnum/=10; // go to next digit;end to start;r to l
cardlength++; //counter to get the length of digits for validation condition
}

bool is_valid=(sum_of_even+sum_of_double_odds)%10==0; // luhn's algorithm
first_two_digits=(digit1*10)+digit2;

if(cardlength==15 && (first_two_digits==34 || first_two_digits==37) && is_valid)
{
printf("AMEX\n");
}
else if(cardlength==16 && first_two_digits >= 51 && first_two_digits <= 55 && is_valid)
{
printf("MASTERCARD\n");
}
else if((cardlength==13  || cardlength==16)&& digit1==4 && is_valid)
{
printf("VISA\n");
}
else
{
printf("INVALID\n");
}
}
