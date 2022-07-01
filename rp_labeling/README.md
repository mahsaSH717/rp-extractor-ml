# Research-Problem Labeling
The "rp_labeling" directory has scripts to build a CRF model and save it, evaluate it on unseen data, and to generate extracted-research-problems from the sentences of unseen data.

## CRF model
 "crf-model-sk.py" script uses annotated sentences provided in "labeled_train_data_set.xlsx" file in "create_labeled_data_sets" directory
  to build a CRF model which is able to tag a given sentence with three specific labels:<br />
  - b_rp : shows the start word in a reaserch-problem phrase
  - i_rp : shows a following word in a resaerch-problem phrase
  - o : shows a word that is not a part of a reserch-problem phrase in a sentence

The input data for feature extraction has a format like this:<br />
  -[('Gated-Attention', 'NN', 'o'), ('Readers', 'NNS', 'o'), ('for', 'IN', 'o'), ('Text', 'NNP', 'b_rp'), ('Comprehension', 'NNP', 'i_rp')]

The "word2features" method in "common_functions.py" will extract various features of each word, as well as 1 and/or 2 words after and/or before it if possible.
Then, these features will be used to build a CRF model using sklearn_crfsuite.CRF method.
  
 The result is a model which is saved to "crf_model.sav" file in the same directory and can be used for evaluating or predicting the labels of new sentences.
 The result of building the model and testing it over 20% of training data is as follows:
 
 ![results](/train-test-result-crf.PNG)

## Evaluate the model
 "evaluate_on_unseen.py" uses the unseen data provided in "labeled_evaluate_data_set.xlsx" and the saved CRF-model to predict the labels of each token in the sentences.
 
  The result of this evaluation is as follows:
 
 ![results](/evaluation-results.PNG)

## Extracting research-problem phrases from unseen sentences
"predict_rp_of_sentence.py" can be used to extract "reaserch-problems" for all sentences in "labeled_evaluate_data_set.xlsx" using the CRF model.<br />
This script saves the results in "unseen_data_predictions.xlsx" file, with these columns: 
 - real rp phrase
 - extracted rp phrase<br />

A part from this file is as follows, where the first column is real research-problem and the second is the extracted values by model:<br /> 

![results](/extracted--vs-real-phrases.PNG)
 
