# Python program to create a simple GUI
# calculator using Tkinter

# import everything from tkinter module
from tkinter import *
import string
from functools import  partial
import random
from nltk.corpus import words
from time import sleep

# uncomment the following nltk for first run
# import nltk
# nltk.download('words')


letters_guessed = []
massive_list = list(words.words())

# generate three levels of word list
easy_list = []
medium_list = []
hard_list = []
for one_word in massive_list:
    if len(one_word) <= 5 and len(one_word) >= 1:
        easy_list.append(one_word)
    elif len(one_word) <= 9 and len(one_word) >= 6:
        medium_list.append(one_word)
    else:
        hard_list.append(one_word)

# globally declare the guess variable
level = ""
random_word = ""
chances = 0

# create a GUI window
master = Tk()
master.title("Hangman Home Screen")
master.geometry("500x600")

difficulty_value_value = StringVar()
target_value = StringVar()
status_value = StringVar()

frameCnt = 30
all_frames = [PhotoImage(file='hangman.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]
frames = all_frames

def underscore_systems(random_word):
    thing = ""
    for i in random_word:
        if i in letters_guessed:
            thing = thing + i
        else:
            thing = thing + "_ "
    return thing

def display_status():
    global chances
    global random_word
    global status_value

    if "_" not in underscore_systems(random_word) and random_word:
        status_value.set("You made it!")
        return

    if random_word == "":
        status_value.set("Pick a level to start.")
        return

    if chances <= 0:
        status_value.set(f"Failed: {random_word}")
    else:
        status_value.set(f"You have {chances} chances")


def press(letter, event= None):
    # point out the global guess variable
    global random_word
    global letters_guessed
    global chances
    global target_value
    global letter_buttons_dict
    global gui

    if ("_" not in underscore_systems(random_word)) and random_word:
        display_status()
        return

    if chances <=0:
        display_status()
        return

    if letter not in random_word and letter not in letters_guessed:

        chances -= 1

        # 9 - chances
        # chances = 9, 10-chances = 1
        # chances = 8, 10-chances = 2
        # chances = 7, 10-chances = 3

        my_label = Label(gui, image=frames[10 - chances])
        my_label.grid(row=5, column=7, rowspan=20)

        global count
        count = 10 - chances

        if chances == 0:
            def play_image(my_label):
                def dynamic():
                    global count
                    count += 1
                    if count < 30: # there are 30 frames; do not go over
                        my_label.config(image=frames[count])
                        my_label.after(100, dynamic)
                dynamic()
            play_image(my_label)

    if letter not in letters_guessed:
        letters_guessed.append(letter)

    target_value.set(underscore_systems(random_word))
    display_status()

    my_button = letter_buttons_dict[letter]
    my_button.configure(bg="blue", fg="black")


def press_difficulty_value(input_level):
    # point out the global guess variable
    global difficulty_value_value
    global status_value
    global random_word
    global chances
    global letters_guessed
    global target_value
    global letter_buttons_dict

    for button_name in letter_buttons_dict:
        my_button = letter_buttons_dict[button_name]
        my_button.configure(bg="red", fg="black")

    # reset to empty
    letters_guessed = []

    if input_level == "Short":
        random_word = random.choice(easy_list).lower()
    elif input_level == "Medium":
        random_word = random.choice(medium_list).lower()
    else:
        random_word = random.choice(hard_list).lower()
    chances = 10

    difficulty_value_value.set(input_level)
    target_value.set(underscore_systems(random_word))
    display_status()

    Label(gui, image=frames[0]).grid(row=5, column=7, rowspan=20)


def gameWidow():
    global difficulty_value_value
    global status_value
    global random_word
    global chances
    global letters_guessed
    global target_value
    global letter_buttons_dict
    global gui


    gui = Toplevel(master)

    # set the background colour of GUI window
    gui.configure(background="light green")

    # set the title of GUI window
    gui.title("Hangman")

    # set the configuration of GUI window
    gui.geometry("1100x600")

    # display difficulty_value, in the 0-th row
    difficulty_value_dict = {}
    difficulty_value_dict["Short"] = ["   Short   ", "black", "green", "Short", 0, 0]
    difficulty_value_dict["Medium"] = ["   Medium   ", "black", "yellow", "Medium", 1, 0]
    difficulty_value_dict["Long"] = ["   Long  ", "black", "red", "Long", 2, 0]

    level_buttons_dict = {}
#button formation
    for button_name in difficulty_value_dict:
        my_button = Button(
            gui,
            text=difficulty_value_dict[button_name][0],
            fg=difficulty_value_dict[button_name][1],
            bg=difficulty_value_dict[button_name][2],
            command=partial(press_difficulty_value, difficulty_value_dict[button_name][3]),
            height=2,
            width=15
        )
        my_button.grid(row=difficulty_value_dict[button_name][4], column=difficulty_value_dict[button_name][5])

        level_buttons_dict[button_name] = my_button
        level_buttons_dict[button_name] = my_button

    # display the actual difficulty level
    k = 4
    difficulty_value_label = Label(gui, text="Difficulty", justify=LEFT)
    difficulty_value_label.grid(column=0, row=k)
    difficulty_value_field = Entry(gui, textvariable=difficulty_value_value, state="disabled")
    difficulty_value_field.grid(column=1, row=k)

    # display the guessed word, in the 2-th row
    target_label = Label(gui, text="Target", anchor="w")
    target_label.grid(column=0, row=7)
    target_field = Entry(gui, textvariable=target_value, state="disabled")
    target_field.grid(column=1, row=7)

    # display status like how many times a user can try
    status_label = Label(gui,text="Status", anchor="w")
    status_label.grid(column=0, row=8)
    status_field = Entry(gui, textvariable=status_value, state="disabled")
    status_field.grid(column=1, row=8)


    # display the letter button you can pick
    letter_buttons_dict = {}
    for button_name in string.ascii_lowercase:
        row = (ord(button_name) - ord("a")) // 3 + 10
        col = (ord(button_name) - ord("a")) % 3 + 3

        my_button = Button(
            gui,
            text= " " + button_name + " ",
            fg="black",
            bg="red",
            command=partial(press, button_name),
            height=2,
            width=15
        )
        my_button.grid(row=row, column=col)

        gui.bind(f"<{button_name}>", partial(press, button_name))

        letter_buttons_dict[button_name] = my_button


# Driver code
if __name__ == "__main__":

    label = Label(master, text= "Welcome")


    # instructions
    k = 1
    Label(master, text="Instructions", anchor="nw").grid(column=0, row=k)
    k += 1
    Label(master, text="1. Start game with a level", anchor="nw").grid(column=1, row=k)
    k += 1
    Label(master, text="2. Restart game with a level", anchor="nw").grid(column=1, row=k)
    k += 1
    Label(master, text="3. Duplicate letters do not count", anchor="nw").grid(column=1, row=k)
    k += 1
    Label(master, text="4. Status shows the number of chances", anchor="nw").grid(column=1, row=k)
    k += 1
    Label(master, text="5. Once failed, continue game with a level", anchor="nw").grid(column=1, row=k)
    k += 1
    Label(master, text="6. Letters you have already guessed will turn blue", anchor="nw").grid(column=1, row=k)
    k += 1
    Label(master, text="7. All levels have 10 chances", anchor="nw").grid(column=1, row=k)
    k += 1
    Label(master, text="8. All letters must be lowercase, you may use your keyboard", anchor="nw").grid(column=1, row=k)

    # a button widget which will open a
    # new window on button click
    btn = Button(master,
            text="Play",
            height= 10, width = 20,
            command=gameWidow
    ).grid(row=0, column=0,)


    # start the GUI
    master.mainloop()


