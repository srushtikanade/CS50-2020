#include<cs50.h>
#include<stdio.h>
#include<string.h>
#include<ctype.h>
#include<math.h>

int main(void)

{
    string text = get_string("text:\n");

    // to count letters
    float letters = 0;
    float words = 1;
    float sent = 0;
    int i= 0 ;
    

   for(i=0;i<strlen(text);i++)
      {if (isalpha(text[i]))
    { letters++;
    }

    // to count words
   if( isspace(text[i]))
      { words++;

    }

    // to count sentences
      if (text[i] == '.' || text[i] == '!' || text[i] == '?')
    { sent++;

    }
 }
   //  printf("letters: %f; words: %f; sentences: %f\n", letters, words, sent);
    { float l = letters / words * 100;
    float s = sent / words * 100;
    float index = 0.0588 * l - 0.296 * s - 15.8;
    int g= round(index);
     
   // printf("index rounded:%i\n",g);

if (g >= 1 && g <=16)
        {
            printf("Grade %i\n",g);
        }
    else
    {
        if (g < 1)
        {
            printf("Before Grade 1\n");
        }
        if (g > 16)
        {
            printf("Grade 16+\n");
        }
}
}
}
