class Employee:
    company = "ITC"
    name = "Default Name"
    salary = "def salary"
    def show(self):
        print(f"The name is {self.name} and the salar is {self.salary}")

# class Programmer:
#     company = "ITC InfoTech"
#     def show(self):
#         print(f"The name is {self.name} and the salary is {self.salary}")

#     def showLanguage(self):
#         print(f"The name is {self.name}. and he is good with {self.language}")

class Coder:
    language = "Python"

    def printlanguage(self):
        print(f"Out of all the languages your language is {self.language}")

class Programmer(Employee, Coder):
    company = "ITC InfoTech"
    def showLanguage(self):
        print(f"The name is {self.company}. and he is good with {self.language}")


a = Employee()
b = Programmer()

# b.show()
b.printlanguage()
b.showLanguage()