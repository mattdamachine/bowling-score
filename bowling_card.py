from tkinter import *
from tkinter import messagebox

window = Tk()
window.title('Bowling Score Card')
window.geometry('900x300')

# Initial Variables
CURRENT_FRAME = 0
FIRST_ROLL = 0
SECOND_ROLL = 0
STRIKE_COUNT = 0
IS_FIRST_ROLL = True
IS_SPARE = False
IS_TENTH_FRAME = False
TOTAL_SCORE = 0

# Function to calculate the stacked strike score
def strike_calc(first_roll, second_roll):
    global STRIKE_COUNT, TOTAL_SCORE

    if STRIKE_COUNT > 0:
        while STRIKE_COUNT >= 3:
            TOTAL_SCORE += 30
            SCORES[CURRENT_FRAME-STRIKE_COUNT].config(text=str(TOTAL_SCORE))
            STRIKE_COUNT -= 1
        if STRIKE_COUNT == 2:
            TOTAL_SCORE += (20 + first_roll)
            SCORES[CURRENT_FRAME-STRIKE_COUNT].config(text=str(TOTAL_SCORE))

        TOTAL_SCORE += (10 + (first_roll + second_roll))
        SCORES[CURRENT_FRAME-1].config(text=TOTAL_SCORE)
        STRIKE_COUNT = 0

# Function to calculate the spare score
def spare_check():
    global IS_SPARE, TOTAL_SCORE
    if IS_SPARE:
        TOTAL_SCORE += (FIRST_ROLL + 10)
        SCORES[CURRENT_FRAME - 1].config(text=str(TOTAL_SCORE))
        IS_SPARE = False

# Function to reset all the score widgets and variables 
# Prompts the user if they want to play again
def end_game():
    global CURRENT_FRAME, FIRST_ROLL, SECOND_ROLL, STRIKE_COUNT
    global IS_FIRST_ROLL, IS_SPARE, IS_TENTH_FRAME, TOTAL_SCORE

    # Show the user their final score and ask them if they want to play again
    response = messagebox.askyesno("Game Over", "Great Game! You bowled a score of " + str(TOTAL_SCORE) +
                                   '.\n Would you like to bowl again?')
    if response:
        # Clear all the pin counts and scores on the card
        frame1pins.config(text=' ')
        frame1score.config(text=' ')
        frame2pins.config(text=' ')
        frame2score.config(text=' ')
        frame3pins.config(text=' ')
        frame3score.config(text=' ')
        frame4pins.config(text=' ')
        frame4score.config(text=' ')
        frame5pins.config(text=' ')
        frame5score.config(text=' ')
        frame6pins.config(text=' ')
        frame6score.config(text=' ')
        frame7pins.config(text=' ')
        frame7score.config(text=' ')
        frame8pins.config(text=' ')
        frame8score.config(text=' ')
        frame9pins.config(text=' ')
        frame9score.config(text=' ')
        frame10pins.config(text=' ')
        frame10score.config(text=' ')

        # Set all the variables back to their default settings
        CURRENT_FRAME = 0
        FIRST_ROLL = 0
        SECOND_ROLL = 0
        STRIKE_COUNT = 0
        IS_FIRST_ROLL = True
        IS_SPARE = False
        IS_TENTH_FRAME = False
        TOTAL_SCORE = 0
        PinPrompt.config(text='How many pins were knocked down on the first roll?')

# Main Function
def bowl():
    global FIRST_ROLL, SECOND_ROLL, IS_FIRST_ROLL, CURRENT_FRAME
    global TOTAL_SCORE, IS_SPARE, STRIKE_COUNT, IS_TENTH_FRAME

    # Conditional Statement for the Tenth Frame Only
    if IS_TENTH_FRAME:
        THIRD_ROLL = PinEntry.get()
        TOTAL_SCORE += int(THIRD_ROLL)
        FRAMES[CURRENT_FRAME].config(text=str(FIRST_ROLL) + '-' + str(SECOND_ROLL) + '-' + THIRD_ROLL)
        SCORES[CURRENT_FRAME].config(text=TOTAL_SCORE)
        PinEntry.delete(first=0, last=2)
        end_game()
        return

    # First Roll
    elif IS_FIRST_ROLL:
        FIRST_ROLL = int(PinEntry.get())
        # If a strike was rolled on the first ball and it's not the 10th frame
        if FIRST_ROLL == 10 and CURRENT_FRAME != 9:
            FRAMES[CURRENT_FRAME].config(text='X')
            spare_check()
            STRIKE_COUNT += 1
            CURRENT_FRAME += 1
        # Else a strike was not rolled and a second roll is given
        else:
            spare_check()
            FRAMES[CURRENT_FRAME].config(text=str(FIRST_ROLL) + '-')
            PinPrompt.config(text='How many pins were knocked down on the second roll?')
            IS_FIRST_ROLL = False
        PinEntry.delete(first=0, last=2)
    # Second Roll
    else:
        SECOND_ROLL = int(PinEntry.get())
        strike_calc(FIRST_ROLL, SECOND_ROLL)  # Were Strikes previously rolled?
        # if a spare was rolled and it's not the 10th frame
        if SECOND_ROLL == (10 - FIRST_ROLL) and CURRENT_FRAME != 9:
            FRAMES[CURRENT_FRAME].config(text=str(FIRST_ROLL) + '-/')
            IS_SPARE = True
        else:  # Update the score with the pins knocked down
            FRAMES[CURRENT_FRAME].config(text=str(FIRST_ROLL) + '-' + str(SECOND_ROLL))
            TOTAL_SCORE += FIRST_ROLL + SECOND_ROLL
            SCORES[CURRENT_FRAME].config(text=str(TOTAL_SCORE))

        # If tenth frame and a third roll is allowed
        if CURRENT_FRAME == 9 and (FIRST_ROLL == 10 or FIRST_ROLL + SECOND_ROLL == 10):
            PinPrompt.config(text='How many pins were knocked down on the third roll?')
            PinEntry.delete(first=0, last=2)
            IS_TENTH_FRAME = True
        else:  # Else cycle back to the first roll
            PinPrompt.config(text='How many pins were knocked down on the first roll?')
            PinEntry.delete(first=0, last=2)
            IS_FIRST_ROLL = True
            CURRENT_FRAME += 1
            if CURRENT_FRAME == 10:
                end_game()


#################### Tkinter widget setup ####################

Prompts = Frame(window)
Prompts.grid(row=0, column=0)

PinPrompt = Label(Prompts, text='How many pins were knocked down on the first roll?')
PinPrompt.grid(row=0, column=0, columnspan=1)

PinEntry = Entry(Prompts, width=10)
PinEntry.grid(row=0, column=1, columnspan=1, sticky=W)

BowlButton = Button(Prompts, text='BOWL', command=bowl)
BowlButton.grid(row=0, column=2, sticky=W)

Frames = Frame(window)
Frames.grid(row=1, column=0)

'''1'''
# The Frame
frame1 = LabelFrame(Frames, text='1', padx=7, pady=40, labelanchor='n')
frame1.grid(row=1, column=0)
# Inside frame to hold the pins knocked down during the current frame
frame1pinframe = Frame(frame1, bd='2p', height=70, width=70, bg='white')
frame1pinframe.pack(side=TOP)
# Stop the frame from resizing
frame1pinframe.pack_propagate(False)
# Pin count for the frame
frame1pins = Label(frame1pinframe, text='-', padx=30, pady=20, font=('Helvetica', 20))
frame1pins.pack()
# Current total score
frame1score = Label(frame1, text=' ', pady=10, font=('Helvetica', 40))
frame1score.pack(side=BOTTOM)

'''2'''
frame2 = LabelFrame(Frames, text='2', padx=7, pady=40, labelanchor='n')
frame2.grid(row=1, column=1)

frame2pinframe = Frame(frame2, bd='2p', height=70, width=70, bg='white')
frame2pinframe.pack(side=TOP)
frame2pinframe.pack_propagate(False)

frame2pins = Label(frame2pinframe, text='-', padx=30, pady=20, font=('Helvetica', 20))
frame2pins.pack()

frame2score = Label(frame2, text=' ', pady=10, font=('Helvetica', 40))
frame2score.pack(side=BOTTOM)

'''3'''
frame3 = LabelFrame(Frames, text='3', padx=7, pady=40, labelanchor='n')
frame3.grid(row=1, column=2)

frame3pinframe = Frame(frame3, bd='2p', height=70, width=70, bg='white')
frame3pinframe.pack(side=TOP)
frame3pinframe.pack_propagate(False)

frame3pins = Label(frame3pinframe, text='-', padx=30, pady=20, font=('Helvetica', 20))
frame3pins.pack()

frame3score = Label(frame3, text=' ', pady=10, font=('Helvetica', 40))
frame3score.pack(side=BOTTOM)

'''4'''
frame4 = LabelFrame(Frames, text='4', padx=7, pady=40, labelanchor='n')
frame4.grid(row=1, column=3)

frame4pinframe = Frame(frame4, bd='2p', height=70, width=70, bg='white')
frame4pinframe.pack(side=TOP)
frame4pinframe.pack_propagate(False)

frame4pins = Label(frame4pinframe, text='-', padx=30, pady=20, font=('Helvetica', 20))
frame4pins.pack()

frame4score = Label(frame4, text=' ', pady=10, font=('Helvetica', 40))
frame4score.pack(side=BOTTOM)

'''5'''
frame5 = LabelFrame(Frames, text='5', padx=7, pady=40, labelanchor='n')
frame5.grid(row=1, column=4)

frame5pinframe = Frame(frame5, bd='2p', height=70, width=70, bg='white')
frame5pinframe.pack(side=TOP)
frame5pinframe.pack_propagate(False)

frame5pins = Label(frame5pinframe, text='-', padx=30, pady=20, font=('Helvetica', 20))
frame5pins.pack()

frame5score = Label(frame5, text=' ', pady=10, font=('Helvetica', 40))
frame5score.pack(side=BOTTOM)

'''6'''
frame6 = LabelFrame(Frames, text='6', padx=7, pady=40, labelanchor='n')
frame6.grid(row=1, column=5)

frame6pinframe = Frame(frame6, bd='2p', height=70, width=70, bg='white')
frame6pinframe.pack(side=TOP)
frame6pinframe.pack_propagate(False)

frame6pins = Label(frame6pinframe, text='-', padx=30, pady=20, font=('Helvetica', 20))
frame6pins.pack()

frame6score = Label(frame6, text=' ', pady=10, font=('Helvetica', 40))
frame6score.pack(side=BOTTOM)

'''7'''
frame7 = LabelFrame(Frames, text='7', padx=7, pady=40, labelanchor='n')
frame7.grid(row=1, column=6)

frame7pinframe = Frame(frame7, bd='2p', height=70, width=70, bg='white')
frame7pinframe.pack(side=TOP)
frame7pinframe.pack_propagate(False)

frame7pins = Label(frame7pinframe, text='-', padx=30, pady=20, font=('Helvetica', 20))
frame7pins.pack()

frame7score = Label(frame7, text=' ', pady=10, font=('Helvetica', 40))
frame7score.pack(side=BOTTOM)

'''8'''
frame8 = LabelFrame(Frames, text='8', padx=7, pady=40, labelanchor='n')
frame8.grid(row=1, column=7)

frame8pinframe = Frame(frame8, bd='2p', height=70, width=70, bg='white')
frame8pinframe.pack(side=TOP)
frame8pinframe.pack_propagate(False)

frame8pins = Label(frame8pinframe, text='-', padx=30, pady=20, font=('Helvetica', 20))
frame8pins.pack()

frame8score = Label(frame8, text=' ', pady=10, font=('Helvetica', 40))
frame8score.pack(side=BOTTOM)

'''9'''
frame9 = LabelFrame(Frames, text='9', padx=7, pady=40, labelanchor='n')
frame9.grid(row=1, column=8)

frame9pinframe = Frame(frame9, bd='2p', height=70, width=70, bg='white')
frame9pinframe.pack(side=TOP)
frame9pinframe.pack_propagate(False)

frame9pins = Label(frame9pinframe, text='-', padx=30, pady=20, font=('Helvetica', 20))
frame9pins.pack()

frame9score = Label(frame9, text=' ', pady=10, font=('Helvetica', 40))
frame9score.pack(side=BOTTOM)

'''10'''
frame10 = LabelFrame(Frames, text='10', padx=7, pady=40, labelanchor='n')
frame10.grid(row=1, column=9)

frame10pinframe = Frame(frame10, bd='2p', height=70, width=70, bg='white')
frame10pinframe.pack(side=TOP)
frame10pinframe.pack_propagate(False)

frame10pins = Label(frame10pinframe, text='-', padx=30, pady=20, font=('Helvetica', 20))
frame10pins.pack()

frame10score = Label(frame10, text=' ', pady=10, font=('Helvetica', 40))
frame10score.pack(side=BOTTOM)

# List of all of the pin counts for each frame to be updated
FRAMES = [frame1pins, frame2pins, frame3pins, frame4pins, frame5pins,
          frame6pins, frame7pins, frame8pins, frame9pins, frame10pins]

SCORES = [frame1score, frame2score, frame3score, frame4score, frame5score,
          frame6score, frame7score, frame8score, frame9score, frame10score]

window.mainloop()