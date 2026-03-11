def game():
    elements = int(input("Enter no. of elements: "))
    score=0
    for i in range(elements):
        a = input("Press  S key to increase score.")
        print(a)
        score+=1
    
    f = open("game.txt", "w")
    if score>0:
        f.write(f"High Score, {score}")
    f.close()

game()