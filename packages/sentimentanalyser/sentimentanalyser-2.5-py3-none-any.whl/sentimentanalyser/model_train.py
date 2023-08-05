import os
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from tqdm import tqdm

from sentimentanalyser import preprocess


class Train:

    def pre_process_data(self, df):

        column_name = df.columns[0]
        data = df
        pre_processor = preprocess.PreProcess(data, column_name)    

        data = pre_processor.clean_html()
        data = pre_processor.remove_non_ascii()
        data = pre_processor.remove_spaces()
        data = pre_processor.remove_punctuation()
        data = pre_processor.stemming()
        data = pre_processor.lemmatization()
        data = pre_processor.stop_words()
        return data

    def get_train_vectors(self, data, storage_location):
        col1 = data.columns[0]
        col2 = data.columns[1]
        tfidf_transformer = TfidfVectorizer(min_df=1)
        train_vectors = tfidf_transformer.fit_transform(data[col1])
        joblib.dump(tfidf_transformer, os.path.join(storage_location, 'vectorizer.pkl'))
        
        return train_vectors

    def get_name_instance_all_classifiers(self):
        """
        input: None
        :return: Classifier with name and default params
        """

        classifiers = [
            KNeighborsClassifier(3),
            SVC(kernel="linear", C=0.025),
            SVC(gamma=2, C=1),
            DecisionTreeClassifier(max_depth=5),
            RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
            MLPClassifier(alpha=1),
            MultinomialNB()
        ]

        names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
                 "Random Forest", "Neural Net",
                 "Naive Bayes"]

        return classifiers, names

    def train_file_model(self, file_path, output_path, usable_columns=None):

        data_frame = pd.read_csv(file_path)
        data = self.pre_process_data(data_frame)

        ###############################################################################
        # Set up storage areas
        ###############################################################################

        folder, filename_no_extn = os.path.split(file_path)
        filename_no_extn = filename_no_extn.split('.')[0]

        storage_location = os.path.join(str(Path(output_path)), filename_no_extn)

        print('storage location', storage_location)
        if not os.path.exists(storage_location):
            os.makedirs(storage_location)
            print('Directory ', storage_location,  'Created')
        else:
            print('Directory ', storage_location,  'already exists')

        ###############################################################################
        # Feature extraction
        ###############################################################################
        
        train_vectors = self.get_train_vectors(data, storage_location)

        # why only 2 columns all the time? what if the file has more than 2 columns?
        if usable_columns is not None:
            col1 = usable_columns[0]
            col2 = usable_columns[1]
        else:
            col1 = data.columns[0]
            col2 = data.columns[1]

        ###############################################################################
        # Perform classification with a host of classifiers
        ###############################################################################

        classifiers, names = self.get_name_instance_all_classifiers()
        for name, model in tqdm(zip(names, classifiers)):
            print('Training model:', name)
            name = name.replace(' ', '_')
            model.fit(train_vectors, data_frame[col2])
            print('Saving pickle model file at location:', os.path.join(storage_location, str(name)+'.pkl'))
            joblib.dump(model, os.path.join(storage_location, str(name)+'.pkl'))

        data_frame.to_csv(str(file_path)+'_training_file.csv')
        print('Training successfully completed')

