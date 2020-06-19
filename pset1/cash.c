#include<cs50.h>
#include<math.h>
#include<stdio.h>
int main(void)
{
    float b;
do
{
    b=get_float("change owed:\n");
}
while(b<=0.00);
{ 
    int cents= round(b* 100);
{
int coins=0;
while(cents>=25)
{ coins++;
cents=cents-25;
}
while(cents>=10)
{ coins++;
cents=cents-10;
}
while(cents>=5)
{ coins++;
cents=cents-5;
}
while(cents>=1)
{ coins++;
cents=cents-1;
}
{
printf("%i\n",coins);
}
}
}
}
