def func(l, remover):
    for i in l:
        l.remove(remover)
        return l
    
l = ["Harry", "Rohan", "Hello", "an"]
remover = "an"
print(func(l, remover))
print(l)