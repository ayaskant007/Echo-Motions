class Programmer:
    def __init__(self, name, level, salary, lang):
        self.name = name
        self.level = level
        self.salary = salary
        self.lang = lang

harry = Programmer("Harry", "SDE I", 120000, "Py")
rohan = Programmer("Rohan", "SDE II", 1100000, "C#")

print(harry.name, harry.level, harry.salary, harry.lang)
print(rohan.name, rohan.level, rohan.salary, rohan.lang)