import streamlit as st

st.chat_message("human")
x=st.button("Game") 
print(x)
sth=st.text_input("Write ur text here")
st.write(f"{sth}")