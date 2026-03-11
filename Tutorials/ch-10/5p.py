import random
from random import randint

class Train:

    def __init__(self, trainno):
        self.trainno = trainno
    def book(self, fro, to):
        print(f" The train number is {self.trainno}, and it is going from {fro} to {to}")
    
    def status(self):
        print(f"The status of the train w/ train no {self.trainno} is Running.")

    def getFare(self, fro, to):
        print(f"The fare of the train w.o train no {self.trainno} going from {fro} to {to} is {randint(222, 555)} INR")


train = Train(123599)
train.book("Rampur", "Delhi")
train.status()
train.getFare("Rampur", "Delhi")