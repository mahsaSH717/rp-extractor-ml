# Creating Labeled Dataset
  Creating labeled dataset Excel files from original datasets
  
## Description

1. Creating labeled dataset Excel files from original datasets
   - "create_labeled_data_sets" directory contains the original train and test datasets, and script to build desire Excel datasets for sequence labeling

   - The original train dataset : [training_data](https://github.com/ncg-task/training-data).
   - The original test(evaluation) dataset : [test_data](https://github.com/ncg-task/test-data).
   - In both original datasets some records had missed [],causing problems in processing them. these records have been founded
   and corrected, resulting in "input-data","unseen-data" folders as original datasets in this project.

   - running "create-annotated-data-set-from-jsons.py" script will goes through all folders in original datasets(train/test), looking for research-problem.json
files, and generates equivalent Excel file containing the research-problem phrase, the sentence and labeled sentence

   - For example considering this research-problem.json :
     -  {"has research problem" :
            [["Text Comprehension", {"from sentence" : "Gated - Attention Readers for Text Comprehension"}]]<br />
            } <br />The Excel file equivalent row is: where <B_RP> tag shows the beginning word of a rp-phrase and <I_RP> tag shows the following words of a rp-phrase<br /> 
           
            
            research_problem	 sentence	                                         annotated_sentence
            Text Comprehension	 Gated - Attention Readers for Text Comprehension	<document>Gated-Attention Readers for <B_RP>Text</B_RP> <I_RP>Comprehension</I_RP></document>
            
   - The result labeled train dataset is "labeled_train_data_set.xlsx" and the result test dataset file is "labeled_evaluate_data_set.xlsx"<br />
   I will use these excel files to train a crf model and to evaluate it.
![image](https://user-images.githubusercontent.com/45291684/176881622-8b411591-63be-4650-b9f3-933f4a122f97.png)

![image](https://user-images.githubusercontent.com/45291684/176881527-eeeaee18-d937-475a-b890-5ee4090da14e.png)

