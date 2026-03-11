class Employee:
    company = "ITC"
    def show(self):
        print(f"The name is {self.name} and the salar is {self.salary}")

# class Programmer:
#     company = "ITC InfoTech"
#     def show(self):
#         print(f"The name is {self.name} and the salary is {self.salary}")

#     def showLanguage(self):
#         print(f"The name is {self.name}. and he is good with {self.language}")


class Programmer(Employee):
    company = "ITC InfoTech"
    def showLanguage(self):
        print(f"The name is {self.name}. and he is good with {self.language}")


a = Employee()
b = Programmer

print(a.company, b.company)