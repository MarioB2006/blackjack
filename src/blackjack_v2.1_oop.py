import random
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier 

import numpy as np
import pandas as pd

class Bot:
    def __init__(self,k:int,stack:int,player:Player):
        self.stack=stack
        self.k=k 
        self.knn=KNeighborsClassifier(self.k) 
        self.player=player
    def difficulty(self:Bot,string:str)->str:
        if string=="easy":
            return "easy.csv"
        elif string=="medium":
            return "medium.csv"
        elif string=="hard":
            return "hard.csv"
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
        prediction=self.predict(st.session_state.player_stack,self.stack)
        while prediction[0]!=0 and self.stack<21:
            prediction = self.predict(st.session_state.player_stack,self.stack)
            self.stack+=random.randint(1,10)
        return self.stack
    def game_states(self:Bot)->int:
        if self.stack<=21:
            if self.stack<st.session_state.player_stack:
                return 1
            elif self.stack==st.session_state.player_stack:
                return 2    
            else:
                return 3
        else:
            return 4 

class Player:
    def __init__(self:Player,count:list):
        self.count=count
    
class Web_app:
    def __init__(self:Web_app,player:Player,bot:Bot):
        self.player = player
        self.bot = bot
    def setup(self):
        if "player_stack" not in st.session_state:
            st.session_state.player_stack =0
        if "bot_stack" not in st.session_state:
            st.session_state.bot_stack = self.bot.stack
        if "draw_value" not in st.session_state:
            st.session_state.draw_value = 0
        if "bot_status_text" not in st.session_state:
            st.session_state.bot_status_text = "bot stack: 0"
        if "user_stack_text" not in st.session_state:
            st.session_state.user_stack_text= f"current stack: {st.session_state.player_stack}"
        if "user_drawed_number" not in st.session_state:
            st.session_state.user_drawed_number=f"Your draw: "
        if "game_status_text" not in st.session_state:
            st.session_state.game_status_text = ""
        if "b1_status" not in st.session_state:
            st.session_state.b1_status=False
        if "b2_status" not in st.session_state:
             st.session_state.b2_status=False
        if "b3_status" not in st.session_state:
            st.session_state.b3_status=False
        if "b5_status" not in st.session_state:
            st.session_state.b5_status=False
        if "choice" not in st.session_state:
            st.session_state.choice=False
        if "score" not in st.session_state:
            st.session_state.score = [0, 0] 
        if "difficulty" not in st.session_state:
            st.session_state.difficulty = None


        st.markdown(
        """
            <style>
                .title {
                    font-size: 40px;
                    font-family: cursive, fantasy;
                    text-align: center;
                    color: #C20827 !important;
                }
                .stApp {
                    background-image: url("https://wallpapers.com/images/high/neutral-color-background-2880-x-1232-vrptue2wa1k87t7l.webp");
                    background-size: cover;
                }
            </style>
        """, 
        unsafe_allow_html=True)
        st.markdown('<div class="title">BLACKJACK</div><br><br>', unsafe_allow_html=True)
        col1, col2 = st.columns([2.5,1])
        
        width=200

        with col1:
            button1 = st.button("draw",width=width,on_click=lambda:drawing(),disabled=st.session_state.b1_status)
            button2 = st.button("stop drawing",width=width,on_click=lambda:drawing_bot(),disabled=st.session_state.b2_status)
            button3 = st.button("reset game",on_click=lambda:reset(),width=width,disabled=st.session_state.b3_status)
            st.text_input("Write the difficulty here",key="difficulty",width=width,on_change=lambda:player_choice(),disabled=st.session_state.choice)
            button5 = st.button("end game",width=width,on_click=lambda:st.stop())
    
        with col2:
            label1 = st.markdown(f"<p style='font-size:20px; font-family:cursive,fantasy;'>{st.session_state.score}</p>", unsafe_allow_html=True)
            label2 = st.markdown(f"<br><p style='font-size:20px; font-family:cursive,fantasy;'>{st.session_state.user_drawed_number}</p>", unsafe_allow_html=True)
            label3 = st.markdown(f"<p style='font-size:20px; font-family:cursive,fantasy;'>{st.session_state.user_stack_text}</p>", unsafe_allow_html=True)
            label4 = st.markdown(f"<p style='font-size:20px; font-family:cursive,fantasy;'>{st.session_state.bot_status_text}</p><br>", unsafe_allow_html=True)
            label5 = st.markdown(f"<p style='font-size:20px; font-family:cursive,fantasy;'>{st.session_state.game_status_text}</p>",unsafe_allow_html=True)

        def reset():
            st.session_state.player_stack = 0
            st.session_state.bot_stack = 0
            st.session_state.draw_value = 0
            st.session_state.bot_status_text = "bot stack: 0"
            st.session_state.user_stack_text = "current stack: 0"
            st.session_state.user_drawed_number = "Your draw: "
            st.session_state.game_status_text = ""
            st.session_state.b1_status = False
            st.session_state.b2_status = False
            st.session_state.b3_status = False
            st.session_state.b5_status = False
            self.bot.stack = 0

        def player_choice():
            try:
                difficulty= st.session_state.difficulty.strip().lower()
                path=self.bot.difficulty(difficulty)
                l1,l2=self.bot.load_data(path)
                self.bot.learning(l1,l2)
            except ValueError:
                st.session_state.game_status_text=f"failed to load difficulty"
            finally:
                st.session_state.choice=True

        def drawing_bot():
            stack_bot=self.bot.draw_card()
            st.session_state.bot_stack=stack_bot
            st.session_state.b2_status=True 
            st.session_state.bot_status_text = f"bot stack: {st.session_state.bot_stack}"
            state_games()

        def drawing():
            draw = random.randint(1,10)
            st.session_state.player_stack += draw
            if st.session_state.player_stack>21:
                st.session_state.game_status_text=f"over 21, you lost"
                st.session_state.score[0]+=1
                update_score()
                st.session_state.b1_status=True    
                st.session_state.b2_status=True  
                state_games()
            else:
                st.session_state.user_drawed_number = f"Your draw: {draw}"
                st.session_state.user_stack_text = f"current stack: {st.session_state.player_stack}"
                
        def update_score():
            wins = st.session_state.score[1]
            losses = st.session_state.score[0]
            st.session_state.game_state_text = f"[{wins},{losses}]"

        def state_games():
            self.player.stack = st.session_state.player_stack
            self.bot.stack = st.session_state.bot_stack
            game_state = self.bot.game_states()
            if game_state==1:
                st.session_state.game_status_text="user won"
                st.session_state.score[1]+=1
                update_score()
                st.session_state.b1_status=True    
                st.session_state.b2_status=True   
      
            elif game_state==2:
                st.session_state.game_status_text = "no one won"
                update_score()
                st.session_state.b1_status=True    
                st.session_state.b2_status=True 

            elif game_state == 3:
                st.session_state.game_status_text = "bot won"
                st.session_state.score[0] += 1
                update_score()
                st.session_state.b1_status=True    
                st.session_state.b2_status=True 

            else:
                st.session_state.game_status_text = "user won"
                st.session_state.score[1] += 1
                update_score()
                st.session_state.b1_status=True    
                st.session_state.b2_status=True 

class Game:
    def __init__(self):
        pass
    def game_loop(self:Game):
        p1=Player(count=[0,0])
        b1=Bot(k=2,stack=0,player=p1)
        path=b1.difficulty("medium")
        l1,l2=b1.load_data(path)
        b1.learning(l1,l2)
        app=Web_app(p1,b1)
        app.setup()
def main():
    g1=Game().game_loop()

if __name__=="__main__":
    main()
