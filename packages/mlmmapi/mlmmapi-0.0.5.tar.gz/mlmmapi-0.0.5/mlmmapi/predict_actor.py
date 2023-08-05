from fuzzywuzzy import fuzz
import pkg_resources
import joblib
import pandas as pd

model_filename = pkg_resources.resource_filename(__name__, 'predict_actor.xgb')
category_filename = pkg_resources.resource_filename(__name__, 'actors.csv')

def convert_answer( answer, correct_answer, max_size=24) :
    "Convert a string to an array of ascii charactor ordinal values with fuzzy match score appended"
    converted = []
    score = fuzz.ratio(answer, correct_answer)
    for i in range(0, max_size) :
        if i < len(answer) :
            # print("{} {} ord: {}".format(i,  answer[i], ord(answer[i])))
            converted.append(float(ord(answer[i])))
        else :
            converted.append(32.0)
    converted.append(score)
    converted.append(len(answer))
    converted_pd = pd.DataFrame([converted])
    result = converted_pd.rename(columns={25:'length'})

    return result, score

def predict_actor(answer, correct_answer):
    filename = model_filename
    model = joblib.load(filename)

    categories = pd.read_csv(category_filename)
    X, score = convert_answer(answer, correct_answer)
    result = model.predict(X)
    prediction = categories.iloc[result[0]].values[0]
    return categories.iloc[result[0]].values[0], score

def check_answer(answer, correct_answer):
    prediction, score = predict_actor(answer, correct_answer)
    correct = False
    if (prediction == correct_answer) or (score > 95):
        correct = True
    return correct, prediction, score
