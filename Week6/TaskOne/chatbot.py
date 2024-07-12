import os
# Set the environment variable to suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
# Attempt to set TensorFlow logger to ERROR, after setting the environment variable
tf.get_logger().setLevel('ERROR')

import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('Week6/TaskOne/intents.json').read())
words = pickle.load(open('Week6/TaskOne/Assets/words.pkl', 'rb'))
classes = pickle.load(open('Week6/TaskOne/Assets/classes.pkl', 'rb'))
model = load_model('Week6/TaskOne/Assets/chatbot_model.keras')


def cleanUpSentence(sentence):
    sentenceWords = nltk.word_tokenize(sentence)
    sentenceWords = [lemmatizer.lemmatize(word) for word in sentenceWords]
    return sentenceWords

def bagOfWords(sentence):
    sentenceWords = cleanUpSentence(sentence)
    bag = [0] * len(words)
    for s in sentenceWords:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

def predictClass(sentence):
    bow = bagOfWords(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.5

    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    returnList = []
    for result in results:
        returnList.append({'intent': classes[result[0]], 'probability': str(result[1])})
    return returnList

def getResponse(intentsList, intentsJson):
    tag = intentsList[0]['intent']
    list_of_intents = intentsJson['intents']
    for intent in list_of_intents:
        if intent['tag'] == tag:
            result = random.choice(intent['responses'])
            break
    return result

print("Go ahead and ask me something! Type 'q' to exit and 'h' to connect to a real human.")
x = intents['intents']
while True:
    message = input("You: ")
    if message.lower() == 'q':
        break

    if message.lower() == 'h':
        print("Bot: I apologise if I couldn't be of much help. Our associates will contact you soon. Thank you!")
        break

    intentsList = predictClass(message)
    if intentsList:
        result = getResponse(intentsList, intents)
        print("Bot:", result)
    else:
        print("Bot: I'm sorry, I don't understand that. Can you please rephrase? You can always connect to a real human by typing 'human'.")
    
