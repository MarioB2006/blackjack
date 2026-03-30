import random
import tkinter as tk
from ttkbootstrap import Style

from sklearn.neighbors import KNeighborsClassifier 
import numpy as np

easy_data = {
    1: np.array([
        # Original data (kept)
        [5, 3], [10, 5], [12, 10], [14, 12], [15, 14],
        [16, 15], [17, 16], [18, 17], [19, 18], [20, 19],
        [18, 18], [19, 19], [20, 20],
        [5, 15], [7, 16], [10, 17],
        [20, 10], [21, 12], [21, 15],

        # Additional data
        # Early game – both lowx
        [2, 2], [3, 1], [4, 2],
        # Mid game – balanced
        [10, 10], [12, 12], [13, 13], [14, 14], [15, 15],
        # Mid game – user slightly ahead
        [12, 10], [13, 11], [14, 12], [15, 13],
        # Mid game – user behind
        [10, 12], [11, 13], [12, 14], [13, 15],
        # End game – both near 21
        [18, 19], [19, 18], [20, 18], [18, 20], [19, 20],
        # End game – user ahead but risky
        [20, 16], [20, 17], [21, 18],
        # End game – bot ahead but risky
        [16, 20], [17, 20], [18, 21],
        # Borderline stop situations
        [17, 17], [16, 17], [17, 16],
        # Bot behind but user high – still draws (easy)
        [19, 10], [20, 11], [21, 12],
    ]),
    2: np.array([
        # Original labels (kept)
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        1, 1, 1,
        1, 1, 1,
        1, 1, 1,

        # Additional labels (same order as above)
        1, 1, 1,          # early game → draw
        1, 1, 1, 1, 1,    # balanced mid → draw (easy mode draws too much)
        1, 1, 1, 1,       # user ahead → draw to catch up
        1, 1, 1, 1,       # user behind → still draws (easy mode always draws)
        1, 1, 1, 1, 1,    # end game near 21 → still draws (easy mode draws recklessly)
        1, 1, 1,          # user ahead but risky → draw
        1, 1, 1,          # bot ahead but risky → draw
        1, 1, 1,          # borderline → draw (easy mode never stops)
        1, 1, 1,          # bot behind, user high → draw
    ])
}

medium_data = {
    1: np.array([
        # Original data
        [5, 3], [10, 4], [12, 7], [14, 10], [15, 11],
        [16, 12], [17, 13], [18, 14], [19, 15], [20, 16], [21, 17],
        [18, 12], [19, 13], [20, 14],
        [5, 15], [7, 16], [10, 17],
        [20, 20], [21, 20], [21, 19],

        # Additional data
        # Early game
        [2, 2], [3, 1], [4, 2], [6, 3],
        # Mid game balanced
        [10, 10], [11, 11], [12, 12], [13, 13], [14, 14], [15, 15],
        # Mid game user ahead
        [13, 10], [14, 11], [15, 12], [16, 13],
        # Mid game user behind
        [10, 13], [11, 14], [12, 15], [13, 16],
        # End game
        [18, 18], [19, 18], [18, 19], [19, 19], [20, 18], [18, 20],
        # Risky user ahead
        [20, 15], [21, 16], [20, 17],
        # Risky bot ahead
        [15, 20], [16, 20], [17, 21],
        # Borderline
        [16, 16], [17, 17], [16, 17], [17, 16],
        # Bot behind user high – selective draw
        [19, 12], [20, 13], [21, 14],
    ]),
    2: np.array([
        # Original labels
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0,
        1, 1, 1,
        0, 0, 0,
        0, 0, 0,

        # Additional labels
        1, 1, 1, 1,                 # early game → draw
        1, 1, 1, 1, 1, 1,           # balanced mid → stop (medium: stop if close to 21)
        1, 1, 1, 1,                 # user ahead → draw to catch up
        0, 0, 0, 0,                 # user behind → stop (safe)
        0, 0, 0, 0, 0, 0,           # end game → stop (medium stops near 21)
        1, 1, 1,                    # user ahead, risky → draw
        0, 0, 0,                    # bot ahead, risky → stop (medium stops when ahead)
        0, 0, 0, 0,                 # borderline → stop (medium knows when to stop)
        1, 1, 1,                    # bot behind user high → draw if still safe
    ])
}

hard_data = {
    1: np.array([
        # Original data
        [5, 3], [10, 4], [12, 6], [14, 8], [15, 10],
        [16, 12], [17, 13], [18, 14], [19, 15], [20, 16],
        [18, 12], [19, 13], [20, 14], [21, 15],
        [5, 15], [7, 16], [10, 17],
        [20, 20], [21, 19], [21, 20],

        # Additional data
        # Early game – cautious draws
        [2, 2], [3, 1], [4, 2], [5, 4], [6, 5],
        # Mid game balanced – optimal stops
        [10, 10], [11, 11], [12, 12], [13, 13], [14, 14], [15, 15],
        [16, 16], [17, 17],
        # Mid game user ahead – draws only if safe
        [13, 10], [14, 11], [15, 12], [16, 13], [17, 14],
        # Mid game user behind – stops unless very low
        [10, 13], [11, 14], [12, 15], [13, 16], [14, 17],
        # End game – optimal decisions
        [18, 18], [19, 18], [18, 19], [19, 19],
        [20, 18], [18, 20], [20, 19], [19, 20],
        # Risky user ahead – draws only if bot can beat
        [20, 15], [21, 16], [20, 16], [21, 17],
        # Risky bot ahead – always stops
        [15, 20], [16, 20], [17, 20], [18, 20],
        # Borderline – stop unless behind by > 3
        [16, 17], [17, 18], [17, 16], [18, 17],
        # Bot behind user high – draws only if user is not too high
        [19, 12], [20, 13], [20, 14], [21, 15],
    ]),
    2: np.array([
        # Original labels
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0,
        1, 1, 1, 1,
        0, 0, 0,
        0, 0, 0,

        # Additional labels
        1, 1, 1, 1, 1,                # early game → draw (safe)
        1, 1, 1, 1, 1, 1, 0, 0,       # balanced mid → draw only if ≤15, else stop
        1, 1, 1, 1, 1,                # user ahead → draw to catch up (if safe)
        0, 0, 0, 0, 0,                # user behind → stop (hard stops early)
        0, 0, 0, 0, 0, 0, 0, 0,       # end game → stop
        1, 1, 1, 1,                   # user ahead risky → draw only if bot can still win
        0, 0, 0, 0,                   # bot ahead risky → stop
        0, 0, 0, 0,                   # borderline → stop (hard stops on borderline)
        1, 1, 1, 0,                   # bot behind user high → draw only if user <20
    ])
}


root = tk.Tk()                 
style = Style(theme="cyborg") 
root.title("blackjack")
root.geometry("500x650")

label0=tk.Label(text="game state: [0,0]",font=(10))
label0.pack(pady=20)

label1 = tk.Label(text="Your draw: 0",font=(16))
label1.pack(padx=0,pady=10)

label2 = tk.Label(text="current stack: 0",font=(16))
label2.pack(padx=0,pady=10)

label3 = tk.Label(text="bot stack: 0",font=(16))
label3.pack(padx=0,pady=10)

label4 = tk.Label(text="",font=(16))
label4.pack(padx=0,pady=10)

current_stack_user=0
current_stack_bot=0
choice_difficulty=0
count=[0,0]

def get_text():
    global choice_difficulty
    if entry.get()=="easy":
        choice_difficulty=1
    elif entry.get()=="medium":
        choice_difficulty=2
    elif entry.get()=="hard":
        choice_difficulty=3
    else:
        choice_difficulty=404
    entry.delete(0,tk.END)
    button5.config(state="disabled")

def draw():
    random_number=random.randint(1,10)
    label1.config(text=f"Your draw: {random_number}")
    return random_number

def calculate_stack(draws:int):
    global current_stack_user
    global count
    current_stack_user=current_stack_user+draws
    if current_stack_user>21:
        label4.config(text=f"over 21, you lost")
        button1.config(state="disabled")       
        button2.config(state="disabled")       
        count[0]+=1
        label0.config(text=f"game state: {count}")
    else:
        label2.config(text=f"current stack: {current_stack_user}")

def learning_algo(user:int,bot:int)->list:
    x=0
    y=0
    if choice_difficulty==1:
        x = easy_data[1]
        y = easy_data[2]
    elif choice_difficulty==2:
        x = medium_data[1]
        y = medium_data[2]
    elif choice_difficulty==3:
        x = hard_data[1]
        y = hard_data[2]
    else:
        x = medium_data[1]
        y = medium_data[2]

    knn = KNeighborsClassifier(n_neighbors=3) 
    knn.fit(x,y)

    predict_number=np.array([[user,bot]])
    yprediction = knn.predict(predict_number) 
    return yprediction

def bot():
    global count
    global current_stack_bot
    prediction=learning_algo(current_stack_user,current_stack_bot)

    while prediction!=[0] and current_stack_bot<21:
        prediction=learning_algo(current_stack_user,current_stack_bot)
        current_stack_bot += random.randint(1, 10)

    label3.config(text=f"bot stack: {current_stack_bot}")
    if current_stack_bot<=21:
        if current_stack_bot<current_stack_user:
            label4.config(text=f"user won")
            count[1]+=1
            label0.config(text=f"game state: {count}")
            button1.config(state="disabled")       
            button2.config(state="disabled")
        elif current_stack_bot==current_stack_user:
            label4.config(text=f"no one won")
            button1.config(state="disabled")       
            button2.config(state="disabled")      
        else:
            label4.config(text=f"bot won")
            count[0]+=1
            label0.config(text=f"game state: {count}")
            button1.config(state="disabled")       
            button2.config(state="disabled")
    else:
        label4.config(text=f"user won")
        count[1]+=1
        label0.config(text=f"game state: {count}")
        button1.config(state="disabled")       
        button2.config(state="disabled")

def reset():
    global current_stack_bot
    global current_stack_user

    label1.config(text="Your draw: 0")
    label2.config(text="current stack: 0")
    label3.config(text="bot stack: 0")
    label4.config(text="")
    button1.config(state="normal")       
    button2.config(state="normal")

    current_stack_user=0
    current_stack_bot=0

button_width = 15

button1 = tk.Button(root, text="draw",width=button_width, command=lambda:calculate_stack(draw()), font=(10))
button1.pack(pady=5)

button2 = tk.Button(root, text="stop drawing",width=button_width, command=lambda:bot(),font=(10))
button2.pack(pady=5)

button3 = tk.Button(root, text="reset game",width=button_width, command=lambda:reset(), font=(10))
button3.pack(pady=30)

entry=tk.Entry(root)
entry.pack()

button5 = tk.Button(root, text="submit difficulty",width=button_width, command=lambda:get_text(), font=(10))
button5.pack(pady=10)

button4 = tk.Button(root, text="end game",width=button_width, command=root.destroy, font=(10))
button4.pack(pady=25) 

root.mainloop()