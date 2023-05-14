# Import the required Libraries
import gradio as gr
import numpy as np
import pandas as pd
import pickle
from transformers import AutoTokenizer, AutoConfig,AutoModelForSequenceClassification,TFAutoModelForSequenceClassification, pipeline
from scipy.special import softmax

# Requirements
model_path = "KwabenaMufasa/Finetuned-Distilbert-base-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
config = AutoConfig.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

#Preprocess text
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = "@user" if t.startswith("@") and len(t) > 1 else t
        t = "http" if t.startswith("http") else t
        new_text.append(t)
    return " ".join(new_text)

#Process the input and return prediction
def sentiment_analysis(text):
    text = preprocess(text)

    encoded_input = tokenizer(text, return_tensors = "pt") # for PyTorch-based models
    output = model(**encoded_input)
    scores_ = output[0][0].detach().numpy()
    scores_ = softmax(scores_)
    
    # Format output dict of scores
    labels = ["Negative", "Neutral", "Positive"]
    scores = {l:float(s) for (l,s) in zip(labels, scores_) }
    
    return scores

#Gradio app interface
app = gr.Interface(fn = sentiment_analysis,
                   inputs = gr.Textbox("Write your text or tweet here"),
                   outputs = "label",
                   title = "NLP Sentiment Analysis - Zindi Challenge",
                   description  = "Vaccinate or Do Not Vaccinate",
                   interpretation = "default",
                   examples = [["Being vaccinated is actually awesome :)"]]
                   )

app.launch()

