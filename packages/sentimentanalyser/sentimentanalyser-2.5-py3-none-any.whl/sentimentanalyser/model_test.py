import os
from copy import deepcopy
from pathlib import Path

import pandas as pd
from sklearn.externals import joblib
from tqdm import tqdm

from sentimentanalyser import preprocess


class TestData:

    def pre_process_data(self, data):
        # the pre processing part
        column_name = data.columns[0]
        pre_processor = preprocess.PreProcess(data, column_name)
        data = pre_processor.clean_html()
        data = pre_processor.remove_non_ascii()
        data = pre_processor.remove_spaces()
        data = pre_processor.remove_punctuation()
        data = pre_processor.stemming()
        data = pre_processor.lemmatization()
        data = pre_processor.stop_words()

        return data

    def get_name_classifiers(self):

        names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
                 "Random Forest", "Neural Net",
                 "Naive Bayes"]

        return names

    def test_model(self, test_text, test_file_name, test_reference_file, output_dir):

        ###############################################################################
        # Set up source areas/output areas
        ###############################################################################
        refer_filename_extn = test_reference_file
        print("Reference filename without extn is ", refer_filename_extn)

        storage_location = os.path.join(str(Path(output_dir)), refer_filename_extn)
        if not os.path.exists(storage_location):
            print("cannot find pickle files at ", storage_location)

        if test_file_name is not None:
            folder_test, testfile_name_extn = os.path.split(test_file_name)
            testfile_name_extn = testfile_name_extn.split(".")[0]
        else:
            testfile_name_extn = "None"

        # this flag becomes true if test data is a csv file also enables the result dataframe to be written to
        # another csv file you give csv, you get csv

        if test_file_name is None and test_text != "":
            if len(test_text) < 20:
                print("Please provide input large enough, Classifier can understand :)")
                return None, None, False
            else:
                print("Generating the dataframe from text")
                data = {'Text': [test_text]}
                data_frame = pd.DataFrame(data=data)
                print("Done converting string to dataframe")

        # need to consider file
        elif test_file_name is not None and test_text == "":
            print("test file name is ", test_file_name)
            data_frame = pd.read_csv(test_file_name)

        else:
            print("What am i doing here")
            return None, None, False

        data_frame_backup = deepcopy(data_frame)

        vectorizer = os.path.join(Path(storage_location), 'vectorizer.pkl')
        tfidf_transformer = joblib.load(vectorizer)

        print("Loaded vectorizer", vectorizer)

        data = self.pre_process_data(data_frame)

        column1 = data.columns[0]
        data_check = tfidf_transformer.transform(data[column1])

        model_names = self.get_name_classifiers()

        for model_name in tqdm(model_names):
            model_file = os.path.join(storage_location, str(model_name.replace(' ', '_'))+".pkl")
            print("Loading pickled model file at", model_name)
            model = joblib.load(model_file)
            print("Model Loaded from", model_file)
            output = model.predict(data_check)
            data_frame_backup[model_name] = output

        # write to file
        data_frame_backup.to_csv(os.path.join(storage_location, str(testfile_name_extn)+"_results.csv"))
        print("result stored at ", os.path.join(storage_location, str(testfile_name_extn)+"_results.csv"))
        print("_______________________")
        return data_frame_backup

