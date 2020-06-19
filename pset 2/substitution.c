#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include<stdlib.h>

int main(int argc, string argv[])
 {

    // check for 2 arguments only
    if (argc != 2)
    {
        printf(" ./substitution key\n");
        return 1;
    }

    // once I check for correct argv put key into an int k
    string key = (argv[1]);

    // check if the keylength is 26
    if (strlen(key)!=26)
    {
        printf("Nope only 26 letters\n");
        return 1;
    }
//Check for duplicate characters (case-insensitive)
   { int matches = 0;

    for (int i = 0; i<26; i++)
    {
        for (int j = 0; argv[1][j] != '\0'; j++)
        {

            if (argv[1][j] == argv[1][i])
            {
                matches++;
            }
        }
    }
if (matches!= 26)
    {
        printf("do not repeat letters in key\n");
        return 1;
    }
    }

    {
        // prompt user for a code to encrypt
        string plaintext= get_string("enter text:");
        {
// print ciphertext

printf("ciphertext: ");
}


{
//Convert plaintext to ciphertext

    for (int i = 0; i<strlen(plaintext); i++)
    {
        for (int j = 0; j < 26; j++)
        {
if (islower(plaintext[i]))
{
            if (plaintext[i] == 'a' + j)
            {
                    printf("%c", tolower(key[j]));
                }

            }
        else if (isupper(plaintext[i]))
{
if (plaintext[i] == 'A' + j)
          {
                    printf("%c", toupper(key[j]));
                }
            }
        }
        if (!isalpha(plaintext[i]))
        {
            printf("%c", plaintext[i]);
        }
}
//print newline - end of the program
    printf("\n");
    }
    }
    }
