import pickle

import numpy as np
from sklearn.metrics import classification_report

from common_functions import *

labeled_evaluate_data_set_path = "..\create_data_sets\labeled_evaluate_data_set.xlsx"
crf_model_file = 'crf_model.sav'


def evaluate_unseen_data(annotated_evaluate_data):
    labeled_tagged_evaluate_data = generate_labeled_tagged_data(annotated_evaluate_data)

    x_evaluate = [extract_features(data) for data in labeled_tagged_evaluate_data]
    y_evaluate = [get_labels(data) for data in labeled_tagged_evaluate_data]

    # load the model from disk
    loaded_model = pickle.load(open(crf_model_file, 'rb'))
    result = loaded_model.score(x_evaluate, y_evaluate)
    print("re", result)

    y_pred_eval = loaded_model.predict(x_evaluate)

    labels = {"b_rp": 1, "i_rp": 2, "o": 0}

    predictions_ev = np.array([labels[tag] for row in y_pred_eval for tag in row])
    truths_ev = np.array([labels[tag] for row in y_evaluate for tag in row])

    # Print out the classification report
    print(classification_report(
        truths_ev, predictions_ev,
        target_names=["b_rp", "i_rp", "o"]))


if __name__ == '__main__':
    evaluate_unseen_data(labeled_evaluate_data_set_path)
