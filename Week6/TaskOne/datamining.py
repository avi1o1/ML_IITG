import pandas as pd
import json

df = pd.read_csv('Week6/TaskOne/Data/data.csv')
print(df.head())

intents = df.groupby('intent').agg(lambda x: x.tolist()[:69]).reset_index()
intents['tag'] = intents['intent']
intents['patterns'] = intents['instruction']
intents['responses'] = intents['response']
intents = intents[['tag', 'patterns', 'responses']]
intents_dict = intents.to_dict(orient='records')

intents_json = {
    "intents": intents_dict
}

with open('Week6/TaskOne/Data/intents.json', 'w') as f:
    json.dump(intents_json, f)
