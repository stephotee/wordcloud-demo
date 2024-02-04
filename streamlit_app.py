import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.tokenize import word_tokenize
import io
import base64
import pandas as pd

# Initialize NLTK resources
nltk.download('punkt')

# Function to generate word cloud
def generate_word_cloud(text, max_words, color_scheme, text_case, additional_stop_words):
    # Tokenization
    tokens = word_tokenize(text)

    # Stop words removal
    stop_words = set(STOPWORDS).union(set(additional_stop_words))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Text case conversion
    if text_case == 'Upper case':
        tokens = [word.upper() for word in tokens]
    elif text_case == 'Lower case':
        tokens = [word.lower() for word in tokens]

    # Generate word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        max_words=max_words,
        color_func=(lambda *args, **kwargs: color_scheme) if color_scheme != 'black' else None,
        background_color='white'
    ).generate(' '.join(tokens))

    # Display the generated image:
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# Streamlit app layout
st.title('Word Cloud Generator')

# Text input
text_input = st.text_area("Paste text here (use commas to separate words or phrases)")

# File upload
uploaded_file = st.file_uploader("Or upload your data (.csv or .txt)", type=['csv', 'txt'])

# Process uploaded file
if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        text_input = ' '.join(df.iloc[:, 0].astype(str).tolist())
    elif uploaded_file.type == "text/plain":
        text_input = uploaded_file.read().decode('utf-8')

# Side bar for additional controls
max_words = st.sidebar.slider("Number of words", 5, 100, 50, 5)
color_scheme = st.sidebar.selectbox("Text color", options=['black', 'Colorful'])
text_case = st.sidebar.radio("Text case", ('Upper case', 'Lower case'))
additional_stop_words = st.sidebar.text_input("Additional stop words", value='').split(',')

# Custom groups (not fully implemented)
# This part of the code needs to be implemented according to the specifics of the custom grouping functionality

# Button to generate word cloud
if st.button('Generate Word Cloud'):
    color_scheme = 'black' if color_scheme == 'black' else plt.cm.rainbow
    generate_word_cloud(text_input, max_words, color_scheme, text_case, additional_stop_words)

# Download button (not fully implemented)
# Here you need to implement the function to convert the generated word cloud to a PNG and download it
