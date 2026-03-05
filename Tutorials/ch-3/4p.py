a = input("Enter a string: ")

if a.find("  ")!=-1:
    b = a.replace("  "," ")
    print("double space was replaced!") # strings are immutable so a new assignment
    print(b)