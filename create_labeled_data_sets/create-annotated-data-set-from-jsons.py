""" Labeled Dataset Generator

input-data: train dataset that contains research-problem.json files
            in the format of:
            {"has research problem" :
            [["Text Comprehension", {"from sentence" : "Gated - Attention Readers for Text Comprehension"}]]
            }

unseen-data: dataset for evaluation, containing research-problems.json files
             with the same format mentioned above

This script aims to build Excel files with three columns given a train/test dataset root folder:

     1-research_problem: is the mentioned research-problem part in json file :
        "Text Comprehension"

     -sentence: is the value of "from sentence" in json:
        "Gated - Attention Readers for Text Comprehension"

     3-annotated_sentence: is the annotated form of each sentence with tags on "research-problem-phrase".
        For example the annotated value for the above sentence is:
            <document>Gated-Attention Readers for <B_RP>Text</B_RP> <I_RP>Comprehension</I_RP></document>

       <B_RP> tag shows the beginning word of a rp-phrase
       <I_RP> tag shows the following words of a rp-phrase

by running this script train and evaluation Excel files with above format will be generated,
as it calls process_data twice, first to get desired Excel file for train dataset
and second to get the Excel file for evaluate dataset

The results are: labeled_train_data_set.xlsx and labeled_evaluate_data_set.xlsx

functions:

    * process_data - starts Excel file generation
    * extract_data_set_from_json_files - fill Excel file
    * generate_annotated_rp_sentence - generated corresponding tagged sentence
    * pre_process - eliminate redundant spaces affecting tagging result


"""

import glob
import json
import os
import re
import xlsxwriter as xlsxwriter

train_data_set_folder_name = 'input-data'
evaluate_data_set_folder_name = 'unseen-data'
labeled_train_data_set_xlsx = "labeled_train_data_set.xlsx"
labeled_evaluate_data_set_xlsx = "labeled_evaluate_data_set.xlsx"


def process_data(output_file_name, rp_json_root_folder_path):
    """

    :param output_file_name: output Excel file name
    :param rp_json_root_folder_path: dataset folder name containing research problem jsons
    :return: saves the result Excel file
    """

    workbook = xlsxwriter.Workbook(output_file_name)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'research_problem')
    worksheet.write('B1', 'sentence')
    worksheet.write('C1', 'annotated_sentence')
    extract_data_set_from_json_files(rp_json_root_folder_path, worksheet)
    workbook.close()


def extract_data_set_from_json_files(input_folder_name, worksheet):
    """
    This method finds all research-problem json files in the dataset
    and fills the Excel worksheet with proper values from the rp jsons

    :param input_folder_name: dataset root folder name which contains research-problem jsons
    :param worksheet: worksheet to write on

    """

    files = glob.glob(input_folder_name + '/**', recursive=True)
    # itereate over files
    index = 0
    for file in files:

        if file.endswith('research-problem.json'):
            with open(os.path.normpath(file), 'r') as f:
                contents = json.load(f)
                for i in contents['has research problem']:
                    index = index + 1
                    result = generate_annotated_rp_sentence(i)
                    worksheet.write_string(index, 0, ','.join(result[1]))
                    worksheet.write_string(index, 1, i[-1]['from sentence'])
                    worksheet.write_string(index, 2, result[0])


def generate_annotated_rp_sentence(rp_data):
    """

    This method is called by extract_data_set_from_json_files
    for each research problem to generate annotated equivalent

    :param rp_data: a single research problem in a format of
         ["research-problem-phrase", {"from sentence" : "sentence including research-problem-phrase"}]
         take the above sample as an example:
         ["Text Comprehension", {"from sentence" : "Gated - Attention Readers for Text Comprehension"}]
    :return: annotated sentence and the list of research-problem phrases in the sentence
            for example: ["Text Comprehension"],"<document>Gated-Attention Readers for <B_RP>Text</B_RP>
                        <I_RP>Comprehension</I_RP></document>"

    """

    end_index = len(rp_data) - 1
    text = rp_data[-1]['from sentence']
    labels = rp_data[:end_index]
    text = pre_process(text)

    for label in labels:
        label = pre_process(label)
        label_start_index = text.find(label)
        tokens_of_label = label.split()
        for idx, token in enumerate(tokens_of_label[0:], start=0):
            token_index = text.find(token, label_start_index)
            if token_index != -1:
                if idx == 0:
                    text = text[:token_index] + "<B_RP>" + token + "</B_RP>" + text[token_index + len(token):]
                    label_start_index = text.rfind('</B_RP>')
                if 0 < idx < len(tokens_of_label):
                    text = text[:token_index] + "<I_RP>" + token + "</I_RP>" + text[token_index + len(token):]
                    label_start_index = text.rfind('</I_RP>')

    text = "<document>" + text + "</document>"
    return text, labels


def pre_process(text):
    return re.sub(r'(\s([?,.!"]))|(?<=\[|\()(.*?)(?=\)|\])|(\s-\s)', lambda x: x.group().strip(), text)


if __name__ == '__main__':

    process_data(labeled_train_data_set_xlsx, train_data_set_folder_name)
    process_data(labeled_evaluate_data_set_xlsx, evaluate_data_set_folder_name)
