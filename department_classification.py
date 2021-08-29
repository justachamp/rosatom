import pandas as pd
import pickle
import re
from pymystem3 import Mystem


def predict_department(text: str) -> int:
    """
    Predicts target department id for a task

        Input: text. 
            A string containing task description
        Output: department_id. 
            Integer value. 
            One of [ 9,  8,  5, 18, 17, 14, 19, 15, 13, 21, 11, 10]
    """

    preprocessed_text = preprocess(text)
    model = pickle.load(open('models/dep_classification.sav', 'rb'))
    text_for_prediction = [preprocessed_text]
    predicted_department = model.predict(text_for_prediction)[0]

    return predicted_department


def preprocess(text):
    preprocessed_text = words_only(text)
    preprocessed_text = remove_stopwords(preprocessed_text)
    preprocessed_text = lemmatize(preprocessed_text)

    return preprocessed_text


def words_only(text):
    regex = re.compile("[А-Яа-я:=!\)\()\_\%/|]+")

    try:
        return " ".join(regex.findall(text))
    except:
        return ""


def remove_stopwords(text):
    with open('data/stopwords.txt') as filename:
        stopwords = filename.read().split('\n')

    try:
        return " ".join([word for word in text.split() if word not in stopwords])
    except:
        return " "


def lemmatize(text):
    m = Mystem()
    try:
        return "".join(m.lemmatize(text)).strip()
    except:
        return " "
