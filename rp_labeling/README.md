# Reaserch-Problem Labeling
The "rp_labeling" directory has scripts to build a crf model and save it, evaluate it on unseen data, and to generate predicted-research-problems given sentences of unseen data

## CRF model
 "crf-model-sk.py" script uses annotated sentences provided in "labeled_train_data_set.xlsx" file in "create_labeled_data_sets" directory
  to build a crf model which is able to tag a given sentence with three specific labels:<br />
  - b-rp : shows the start word in a reaserch-problem phrase
  - i-rp : shows a following word in a resaerch-problem phrase
  - o : shows a word that is not a part of a reserch-problem phrase in a sentence

  
 The result is a model which is saved to "crf_model.sav" file in the same directory and can be used for evaluating or predicting the labels of new sentences

## Description



![image](https://user-images.githubusercontent.com/45291684/176881527-eeeaee18-d937-475a-b890-5ee4090da14e.png)
