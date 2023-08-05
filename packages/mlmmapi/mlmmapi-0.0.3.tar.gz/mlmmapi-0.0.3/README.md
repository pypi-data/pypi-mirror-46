# interaction-grader
Python package to help grade test questions (interactions) using trained machine learning models.

The Answer class can be used to check if an answer is basically identical to the desired answer except 
for misspellings.

Initial version hard codes a model already trained to recognize actor names from a list of 322.
  
```Python
import mmapi

correct_answer = 'Joaquim Phoenix'
answer = 'Joakim Pheonix'
prediction = predict_actor(answer, correct_answer)  
if prediction == correct_answer  
    print('Correct Answer')  
```

Package Dependencies:  
- fuzzywuzzy  
- python-Levenshtein  
- numpy
- pandas
- sklearn
- xgboost  
