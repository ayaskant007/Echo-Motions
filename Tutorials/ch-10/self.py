class Employee:
    language = "py"
    salary = 1200000

    def getInfo(self):
        print(f"The language is {self.language}.")

    @staticmethod
    def greet():
        print("Good Morning")


harry = Employee()
harry.name = "Harry"
print(harry.name, harry.salary, harry.language)
harry.greet()
harry.getInfo()
