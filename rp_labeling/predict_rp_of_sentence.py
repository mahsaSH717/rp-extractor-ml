import pickle

from common_functions import *

labeled_evaluate_data_set_path = "..\create_data_sets\labeled_train_data_set.xlsx"
crf_model_file = 'crf_model.sav'


def make_prediction_for_unseen_data(unseen_data_file_path):
    evaluate_data_set = pd.read_excel(unseen_data_file_path)

    loaded_model = pickle.load(open(crf_model_file, 'rb'))
    predicted_values = []

    for sent in evaluate_data_set['sentence']:
        labeled_docs_case = []
        tags = []
        sent = pre_process(sent)
        with_out_punctuation_case = remove_punctuation(sent)
        tokenized_sent = word_tokenize(with_out_punctuation_case)
        for token in tokenized_sent:
            tags.append((token, 'o'))
        labeled_docs_case.append(tags)
        labeled_tagged_data = generate_final_data(labeled_docs_case)

        data_test_feats_case = [extract_features(doc) for doc in labeled_tagged_data]
        y_pred_case = loaded_model.predict(data_test_feats_case);

        for x, y in zip(labeled_tagged_data, y_pred_case):
            label = ""
            for x1, y1, in zip(x, y):
                if y1 != 'o':
                    label = label + " " + x1[0]
            predicted_values.append(label)

    df = evaluate_data_set.assign(steals=predicted_values)
    df.to_excel("output2.xlsx")


if __name__ == '__main__':
    make_prediction_for_unseen_data(labeled_evaluate_data_set_path)

