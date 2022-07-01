import pickle
import numpy as np
import sklearn_crfsuite
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from common_functions import *

labeled_train_data_set_path = "..\create_labeled_data_sets\labeled_train_data_set.xlsx"


def build_crf_model(labeled_train_data):
    labeled_tagged_data = generate_labeled_tagged_data(labeled_train_data)
    X = [extract_features(data) for data in labeled_tagged_data]
    y = [get_labels(data) for data in labeled_tagged_data]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=150,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    y_pred = crf.predict(X_test)

    labels = {"b_rp": 1, "i_rp": 2, "o": 0}
    predictions = np.array([labels[tag] for row in y_pred for tag in row])
    truths = np.array([labels[tag] for row in y_test for tag in row])

    print(classification_report(
        truths, predictions,
        target_names=["b_rp", "i_rp", "o"]))

    filename = 'crf_model.sav'
    pickle.dump(crf, open(filename, 'wb'))


if __name__ == '__main__':
    build_crf_model(labeled_train_data_set_path)
