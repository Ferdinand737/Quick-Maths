import tkinter as tk
import random
import re

currentLvl = 1
questionNum = 0
numWrong = 0
numCorrect = 0
percentCorrect = 0
input = ""


def makeQuestion():
    global lastQuestion

    # load current lvl from csv
    global currentLvl

    op = random.uniform(0, 1)
    operator = ""
    intOne = random.randint((6 + currentLvl) * -1, 6 + currentLvl)
    intTwo = random.randint((6 + currentLvl) * -1, 6 + currentLvl)

    if op < 0.25:
        operator = " + "
    if op > 0.25 and op < 0.50:
        operator = " - "
    if op > 0.50 and op < 0.75:
        operator = " * "
    if op > 0.75:
        operator = " / "
        product = intOne * intTwo
        intOne = product

    lastQuestion = "    " + str(intOne) + operator + str(intTwo) + " ="
    return lastQuestion


lastQuestion = makeQuestion()

window = tk.Tk()


def enterKey(event=None):
    global input
    input = textBox.get()

    if (len(input) == 0):
        return

    # Stop Time and Save

    global currentLvl
    global numCorrect
    global questionNum
    global numWrong
    global percentCorrect

    if wasCorrect():
        numCorrect += 1
        questionNum += 1
    else:
        numWrong += 1
        questionNum = 0

    if questionNum == 10:
        currentLvl += 1
        questionNum = 0

    percentCorrect = numCorrect / (numCorrect + numWrong)

    label2["text"] = makeQuestion()
    # Start Timer
    textBox.delete(0, tk.END)
    label3["text"] = retrieveStats()
    label5["text"] = questionsRemaining()
    label4["text"] = retrieveLvl()

    # append csv file with:
    #   DateTime    Current_Lvl      Question    Player_Answered     True_Answer     Was_Correct     Time_To_Answer


def retrieveStats():
    return "Correct:" + str(numCorrect) + "\n" + "Wrong:" + str(numWrong) + "\n" + "Percent Correct:" + str(round(percentCorrect * 100)) + "%"


def retrieveLvl():
    # read lvl from csv file
    return "Current Level: " + str(currentLvl)


def questionsRemaining():
    return str(questionNum) + "/" + str(10)


def wasCorrect():

    global lastQuestion
    nums = [int(i) for i in re.findall(r'-?\d+', lastQuestion)]

    if '+' in lastQuestion:
        solution = nums[0] + nums[1]
    if '-' in lastQuestion:
        solution = nums[0] - nums[1]
    if '*' in lastQuestion:
        solution = nums[0] * nums[1]
    if '/' in lastQuestion:
        solution = nums[0] / nums[1]

    return int(input) == solution


window.title("Quick Maths")

window.geometry("600x250")


# Title
label0 = tk.Label(master=window, text="Solve!",
                  font=('Comic Sans MS', 26, 'bold'))
label0.grid(row=0, column=1)

# Filler
label1 = tk.Label(master=window, text="         ",
                  font=('Comic Sans MS', 26, 'bold'))
label1.grid(row=0, column=2)
# Filler
label1 = tk.Label(master=window, text="         ",
                  font=('Comic Sans MS', 26, 'bold'))
label1.grid(row=1, column=2)

# Stats Title
label1 = tk.Label(master=window, text="Stats",
                  font=('Comic Sans MS', 26, 'bold'))
label1.grid(row=0, column=3)

# Question
label2 = tk.Label(master=window, text=makeQuestion(),
                  font=('Comic Sans MS', 15, 'bold'))
label2.grid(row=1, column=0)

# Entry
textBox = tk.Entry(master=window, width=5, font=('Comic Sans MS', 15, 'bold'))
textBox.grid(row=1, column=1)


# Show feedback in the form of 'Correct!' or 'Answer was:<correct answer>'


# Current Stats
label3 = tk.Label(master=window, text=retrieveStats(),
                  font=('Comic Sans MS', 13))
label3.grid(row=1, column=3)


# Historical Stats
# use Data from csv to make historical stats

# Current level
label4 = tk.Label(master=window, text=retrieveLvl(),
                  font=('Comic Sans MS', 13))
label4.grid(row=3, column=1)

# Questions Remaining
label5 = tk.Label(master=window, text=questionsRemaining(),
                  font=('Comic Sans MS', 13))
label5.grid(row=4, column=1)

# Button
button = tk.Button(text="Submit", font=(
    'Comic Sans MS', 15, 'bold'), command=enterKey)
button.grid(row=2, column=1)

window.bind('<Return>', enterKey)
window.bind('<Enter>', enterKey)

window.mainloop()
