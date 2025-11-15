num1= 0
counter= 0
num1= int(input("Enter first number:"))
while (counter< 2):
    if (num1 % 2== 0):
        counter= counter+ 1
    else: 
        counter= counter- 1
    if (counter== 2):
        break
    num1= int(input("Enter next number:"))
num1= int(num1)
num1= input("Enter another number:")