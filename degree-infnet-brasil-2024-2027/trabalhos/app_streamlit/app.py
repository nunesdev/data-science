import streamlit as st

st.title("Hello")
st.text("texto ciencia de dados")

nome = st.text_input("Digite seu nome:")
st.write(f"{nome}")
st.slider("selecione sua idade",10,100,25)
