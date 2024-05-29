import streamlit as st
import pickle
import string
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

ps=PorterStemmer()

tfidf=pickle.load(open('vectorizor.pkl','rb'))
model=pickle.load(open('spam_model.pkl','rb'))

st.title('SMS Spam Classifier')

input_sms=st.text_input('Enter the message')


def transform_text(text):
    text=text.lower()
    text=nltk.word_tokenize(text)
    
    y=[]
    for i in text:
        if i.isalnum():
            y.append(i)
    text=y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text=y[:]
    y.clear()
    
    for i in text:
        y.append(ps.stem(i))
        
        
    
    return " ".join(y)


if st.button('Predict'):
        
    #preprocess
    transformed_sms=transform_text(input_sms)

    #vectorize
    vector_input=tfidf.transform([transformed_sms])

    #predict
    result=model.predict(vector_input)[0]

    #display
    if result==1:
        st.header("Spam")

    else:
        st.header('Not Spam')