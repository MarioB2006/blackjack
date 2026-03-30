import random
import tkinter as tk
from ttkbootstrap import Style

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier 

import numpy as np
import pandas as pd

class Opponents:
    def __init__(self:Opponents,stack:int):
        self.stack=stack

class Bot(Opponents):
    def __init__(self,k:int,stack:int,player:Player):
        super().__init__(stack)
        self.k=k 
        self.knn=KNeighborsClassifier(self.k) 
        self.player=player
    def difficulty(self:Bot,string:str)->str:
        if string=="easy":
            return "src/easy.csv"
        elif string=="medium":
            return "src/medium.csv"
        elif string=="hard":
            return "src/hard.csv"
        else:
            raise ValueError
    def load_data(self:Bot,path:str)->tuple[list,list]:
        data=pd.read_csv(path)
        user_score=[]
        bot_score=[]
        label=[]
        for items in data["user"]:
            user_score.append(items)
        for items in data["bot"]:
            bot_score.append(items)
        for items in data["label"]:
            label.append(items)
        combined_scores=[list(elements) for elements in zip(user_score,bot_score)]
        return combined_scores,label
    def learning(self:Bot,x:list,y:list):
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        self.knn.fit(X_train, y_train)
        y_pred = self.knn.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        #print("Accuracy:", acc)
    def predict(self:Bot,user_score:int,bot_score:int)->list[int]:
        predict_number=np.array([[user_score,bot_score]])
        yprediction = self.knn.predict(predict_number) 
        return yprediction
    def draw_card(self:Bot)->int:
        random_number=random.randint(1,10)
        self.stack+=random_number
        prediction=self.predict(self.player.stack,self.stack)
        while prediction!=[0] and self.stack<21:
            prediction = self.predict(self.player.stack,self.stack)
            self.stack+=random.randint(1,10)
        return self.stack
    def game_states(self:Bot)->int:
        if self.stack<=21:
            if self.stack<self.player.stack:
                return 1
            elif self.stack==self.player.stack:
                return 2    
            else:
                return 3
        else:
            return 4 

class Player(Opponents):
    def __init__(self:Player,stack:int,count:list):
        super().__init__(stack)
        self.count=count
        self.stack=stack
    def draw_card(self:Player)->tuple[int,int]:
        random_number=random.randint(1,10)
        self.stack+=random_number
        return random_number,self.stack
    
class GUI:
    def __init__(self,bot:Bot,player:Player):
        self.root = tk.Tk()
        self.player = player
        self.bot = bot
    def setup(self):
        style = Style(theme="cyborg") 
        self.root.title(string="Blackjack")
        self.root.geometry("500x650")
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
        button_width = 15
        
        def state_games():
            game_state= self.bot.game_states()
            if game_state==1:
                label4.config(text=f"user won")
                self.player.count[1]+=1
                label0.config(text=f"game state: {self.player.count}")
                button1.config(state="disabled")       
                button2.config(state="disabled")
            elif game_state==2:
                label4.config(text=f"no one won")
                button1.config(state="disabled")       
                button2.config(state="disabled")  
            elif game_state == 3:
                label4.config(text=f"bot won")
                self.player.count[0]+=1
                label0.config(text=f"game state: {self.player.count}")
                button1.config(state="disabled")       
                button2.config(state="disabled")
            else:
                label4.config(text=f"user won")
                self.player.count[1]+=1
                label0.config(text=f"game state: {self.player.count}")
                button1.config(state="disabled")       
                button2.config(state="disabled")

        def drawing():
            current_draw_number,current_stack=self.player.draw_card()
            if current_stack>21:
                label4.config(text=f"over 21, you lost")
                self.player.count[0]+=1
                label0.config(text=f"game state: {self.player.count}")
                button1.config(state="disabled")     
                button2.config(state="disabled")
                label0.config()
            else:
                label1.config(text=f"Your draw: {current_draw_number}")
                label2.config(text=f"current stack: {current_stack}")
 
        button1 = tk.Button(self.root, text="draw",width=button_width, command=lambda:drawing(), font=(10))
        button1.pack(pady=5)

        def drawing_bot():
            stack_bot=self.bot.draw_card()
            label3.config(text=f"bot stack: {stack_bot}")
            button2.config(state="disabled")
            state_games()

        button2 = tk.Button(self.root, text="stop drawing",width=button_width, command=lambda:drawing_bot(),font=(10))
        button2.pack(pady=5)

        def reset():
            label1.config(text="Your draw: 0")
            label2.config(text="current stack: 0")
            label3.config(text="bot stack: 0")
            label4.config(text="")
            button1.config(state="normal")       
            button2.config(state="normal")
            self.bot.stack=0
            self.player.stack=0

        button3 = tk.Button(self.root, text="reset game",width=button_width, command=lambda:reset(), font=(10))
        button3.pack(pady=30)
        entry=tk.Entry(self.root)
        entry.pack()     

        def player_choice():
            try:
                path=self.bot.difficulty(entry.get())
                l1,l2=self.bot.load_data(path)
                self.bot.learning(l1,l2)
            except ValueError:
                label4.config(text="failed to load difficulty")
            finally:
                entry.delete(0,tk.END)
                button5.config(state="disabled")
        
        button5 = tk.Button(self.root, text="submit difficulty",width=button_width, command=lambda:player_choice(), font=(10))
        button5.pack(pady=10)

        button4 = tk.Button(self.root, text="end game",width=button_width, command=self.root.destroy, font=(10))
        button4.pack(pady=25) 
        self.root.mainloop()

class Game:
    def __init__(self):
        pass
    def game_loop(self:Game):
        p1=Player(stack=0,count=[0,0])
        b1=Bot(k=2,stack=0,player=p1)
        path=b1.difficulty("medium")
        l1,l2=b1.load_data(path)
        b1.learning(l1,l2)
        try:
            gui=GUI(bot=b1,player=p1)
            gui.setup()
        except tk.TclError:
            print("failed")

def main():
    g1=Game().game_loop()

if __name__=="__main__":
    main()
