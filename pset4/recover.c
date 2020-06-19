#include<stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 512


int main(int argc, char *argv[])
{
    //Make sure that you have one command line argument
    if (argc != 2)
    {
        printf( "Please enter file to open.\n");
        return 1;
    }

// open memory card file
FILE *file=fopen(argv[1],"r");
if(file == NULL)
{ 
    printf("not a file\n");
}

// set jpg count
int jpg_found=0;

// set filecount
int filecount=0;

// set buffer
unsigned char buffer[BUFFER_SIZE];

// define file for images
FILE *img=NULL;

// set filename 
char filename[8];

// read file
while(fread(buffer,BUFFER_SIZE,1,file)==1) // data,size,qty,file; this condition is satisfied

// check if jpg usinf 1st four bytes
 {
 if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
{
if( jpg_found==1) // already opened a prior jpg byte then close it
{
    fclose(img);
}
else // if not then you found a jpeg so increment counter
{ 
    jpg_found=1;
}

sprintf(filename,"%03i.jpg",filecount); // print filename 000.jpg and increasing each time
img=fopen(filename,"w"); // open file for images to append/write 
filecount++; // after each file is opened increment file count counter
}
if(jpg_found==1) // once found jpeg write from buffer to img file 
{
    fwrite(&buffer,BUFFER_SIZE,1,img);
}
}
fclose(file); // close file(memory card to buffer) and img(buffer to img file)
fclose(img);

// done
return 0;

}
