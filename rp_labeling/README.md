# Reaserch-Problem Labeling
The "rp_labeling" directory has scripts to build a crf model and save it, evaluate it on unseen data, and to generate predicted-research-problems given in the sentences of unseen data

## CRF model
 "crf-model-sk.py" script uses annotated sentences provided in "labeled_train_data_set.xlsx" file in "create_labeled_data_sets" directory
  to build a crf model which is able to tag a given sentence with three specific labels:<br />
  - b_rp : shows the start word in a reaserch-problem phrase
  - i_rp : shows a following word in a resaerch-problem phrase
  - o : shows a word that is not a part of a reserch-problem phrase in a sentence

  
 The result is a model which is saved to "crf_model.sav" file in the same directory and can be used for evaluating or predicting the labels of new sentences
 The results of building the model and testing it over 20% of training data is as follows:
 
 ![results](/train-test-result-crf.PNG)

## Evaluate the model
 "evaluate_on_unseen.py" uses the unseen data provided in "labeled_evaluate_data_set.xlsx" and the saved crf-model to predict the labels of each token in the sentences
 
  The results of this evaluation is as follows:
 
 ![results](/evaluation-results.PNG)

## Extracting research-problem phrases from unseen sentences
"predict_rp_of_sentence.py" can be used to generate extracted "reaserch-problems" for all sentences in "labeled_evaluate_data_set.xlsx" using the CRF model.<br />
This script saves the results in "unseen_data_predictions.xlsx" file, with these columns: 
 - real rp phrase
 - extracted rp phrase<br />

A part from this file is as follows, where the first column is real research-problem and the second is the extraxted values by model:<br /> 

![results](/extracted--vs-real-phrases.PNG)
 

![image](https://user-images.githubusercontent.com/45291684/176881527-eeeaee18-d937-475a-b890-5ee4090da14e.png)
