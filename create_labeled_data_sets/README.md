# Creating Labeled Dataset
  
  Creating labeled dataset Excel files from original datasets<br />
  
  "create_labeled_data_sets" directory contains the original training and test datasets, and an script to build desired Excel datasets for sequence labeling.<br />
  "rp" is sometimes used to refer to "research-problem".
  
## Description

- Creating labeled dataset Excel files from original datasets
   - The original training dataset: [training_data](https://github.com/ncg-task/training-data).
   - The original test(evaluation) dataset: [test_data](https://github.com/ncg-task/test-data).
   - In both original datasets, some records had missed [], causing problems in processing them. These records have been founded
   and corrected, resulting in "input-data"(train), "unseen-data"(test) folders as primitive datasets in this project.

   - running "create-annotated-data-set-from-jsons.py" script will goes through all folders in primitive datasets(train/test), looking for research-problem.json
files, and generates equivalent Excel file containing the research-problem phrase, the sentence, and labeled sentence

   - For example considering this research-problem.json:
     -  {"has research problem" :
            [["Text Comprehension", {"from sentence" : "Gated - Attention Readers for Text Comprehension"}]]}<br />
             <br />The equivalent row in Excel file is as follows, where <B_RP> tag shows the beginning word of a rp-phrase and <I_RP> tag shows the following words of a rp-phrase<br /> 
           
            
            research_problem	 sentence	                                         annotated_sentence
            Text Comprehension	 Gated - Attention Readers for Text Comprehension	<document>Gated-Attention Readers for <B_RP>Text</B_RP> <I_RP>Comprehension</I_RP></document>
            
   - The labeled training dataset file is "labeled_train_data_set.xlsx" and the labeled test dataset file is "labeled_evaluate_data_set.xlsx".<br />I will use these excel files to train a CRF model and evaluate it.

*To move to next part about building the model please check out README file in: [research-problem labeling](rp_labeling)
