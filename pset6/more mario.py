from cs50 import get_int

while True:
        h = get_int("enter a positive integer for height:\n")
        if h > 0 and h<9  :
            break

for i in range(1,h+1):
    nhash=i
    nspace=h-i
    nspace2=i
   # nhash2=h-i
    print(" "*nspace,end="")
    print("#"*nhash,end="")
    print("  ",end="")
    print("#"*nhash,end="")
    print()
