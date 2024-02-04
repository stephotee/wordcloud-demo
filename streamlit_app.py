import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
import pandas as pd
from PIL import Image
import numpy as np
from io import BytesIO

# Required for text processing in NLTK
import nltk
nltk.download('punkt')

# Function to generate a color based on the "Colorful" option
def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h = random_state.randint(0, 360)
    s = int(random_state.rand() * 100)
    l = int(random_state.rand() * 100)
    return f"hsl({h}, {s}%, {l}%)"

# Function to generate word cloud
def generate_word_cloud(text, max_words, color_scheme, text_case, additional_stop_words):
    # Tokenization
    tokens = word_tokenize(text)

    # Stop words removal
    stop_words = set(STOPWORDS).union(set(additional_stop_words))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Text case conversion
    tokens = [word.upper() if text_case == 'Upper case' else word.lower() for word in tokens]

    # Generate word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        max_words=max_words,
        color_func=random_color_func if color_scheme == 'Colorful' else None,
        background_color='white'
    ).generate(' '.join(tokens))

    # Display the generated image:
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

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

# Sidebar for additional controls
max_words = st.sidebar.slider("Number of words", 5, 100, 50, 5)
color_scheme = st.sidebar.selectbox("Text color", options=['black', 'Colorful'])
text_case = st.sidebar.radio("Text case", ('Upper case', 'Lower case'))
additional_stop_words = st.sidebar.text_input("Additional stop words", value='').split(',')

# Button to generate word cloud
if st.button('Generate Word Cloud'):
    generate_word_cloud(text_input, max_words, color_scheme, text_case, additional_stop_words)

# Download button
def get_image_download_link(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="wordcloud.png">Download PNG</a>'
    return href

if 'last_img' in st.session_state:
    st.markdown(get_image_download_link(st.session_state['last_img']), unsafe_allow_html=True)
