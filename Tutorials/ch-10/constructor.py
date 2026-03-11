class Employee:
    language = "py"
    salary = 1200000

    def __init__(self, name, salary, language): #dunder method which is automatically called.
        print("I am creating an object.")
        self.name = name
        self.salary = salary
        self.language = language

    def getInfo(self):
        print(f"The language is {self.language}.")

    @staticmethod
    def greet():
        print("Good Morning")


harry = Employee("Harry", "1300000", "Javascript")
print(harry.name, harry.salary, harry.language)

# rohan = Employee()