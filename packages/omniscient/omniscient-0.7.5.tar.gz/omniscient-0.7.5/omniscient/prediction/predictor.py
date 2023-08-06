import logging
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix
from omniscient.utils.constants import *
from omniscient.utils.file_handler import FileHandler
from deeppavlov.core.common.chainer import Chainer
from typing import List


class Predictor:
    """
    Manipulating data frames and using an initialised model to generate predictions
    """
    def __init__(self, model: Chainer)->None:
        """
        Sets variable model to initialised model object passed in
        :param model: An initialised model
        """
        logging.info("Initialising Predictor")
        self.model = model
        self.file_handler = FileHandler()

    def predict_instance(self, context: str, question: str)->str:
        """
        Returns matched snippet for context and question
        :param context: Context (e.g. document) about which question is asked
        :param question: Question asked
        :return: Matched snippet
        """
        return self.model([context], [question])[0][0]

    def predict_from_file(self, input_file: str, output_file: str)->None:
        """
        Predict labels for each row in a file with the question and sentence on the same row
        :param input_file: File with question and sentence on same row
        :param output_file: File to output DataFrame with Predicted Labels
        """
        try:
            df = self.file_handler.read_dataframe_from_input_file(input_file)
            df_predictions = self.predict_batch(df)  # contains context column
            df_predictions = df_predictions.drop(columns='Context')

            self.file_handler.write_dataframe_to_output_file(df_predictions, output_file)

        except IOError as e:
            logging.error(e)


    def predict_batch(self, df: pd.DataFrame)->pd.DataFrame:
        """
        Predicting on batch of instances (e.g. as converted from a file)
        :param df: Dataframe with QuestionID, Question, Context etc.
        :return: Dataframe with PredictedLabel column attached
        """
        logging.info("Predicting on batch of instances")
        df_contexts = self._create_contexts_dataframe(df)

        # New DataFrame to hold QuestionID and the corresponding predicted answer
        df_qid_ans = pd.DataFrame(columns=['QuestionID', 'PredictedAnswer'])
        for index, row in df_contexts.iterrows():
            # NOTE: pred_ans is the snippet which has the answer, not the whole sentence
            pred_ans = self.predict_instance(row['Context'], row['Question'])
            df_qid_ans = df_qid_ans.append({'QuestionID': row['QuestionID'], 'PredictedAnswer': pred_ans},
                                           ignore_index=True)
            logging.debug("QuestionID: {} Question: {} Predicted Snippet: {}"
                          .format(row['QuestionID'], row['Question'], pred_ans))

        df_with_pred_ans = pd.merge(df, df_qid_ans, on='QuestionID')

        predictions = self._get_prediction_labels(df_with_pred_ans)
        df['PredictedLabel'] = predictions

        logging.info("Precision, Recall, F-Score, Support: {}"
                     .format(precision_recall_fscore_support(df['Label'], df['PredictedLabel'])))
        logging.info("Confusion Matrix: {}".format(confusion_matrix(df['Label'], df['PredictedLabel'])))

        return df

    def _create_contexts_dataframe(self, df:pd.DataFrame)->None:
        """
        Add 'Context' column to the raw dataframe which represents the concatenateion of all the sentences in the file
        :param df: Raw dataframe
        :return: Raw dataframe with 'Context' column added
        """
        # Add new 'context' column which combines all sentences relevant to a Question (to resemble a document)
        df['Context'] = pd.DataFrame(df.groupby(['QuestionID'])['Sentence'].transform(lambda x: ' '.join(x).lower()))

        # Create a new DataFrame with just the QuestionID, Question and the combined text. There will be duplicates
        # equal to the number of sentences - drop these as well
        df_contexts = df[['QuestionID', 'Question', 'Context']].drop_duplicates()

        return df_contexts

    def _get_prediction_labels(self, df_with_pred_ans: pd.DataFrame)->List:
        """
        Check for match of answer snippet string with Sentence for each sentence so that each sentence can be labeled
        as 0 or 1

        :param df_with_pred_ans: DataFrame with 'PredictedAnswer' column
        :return: for each row in DataFrame whether the string in the 'PredictedAnswer' column is found in the sentence
        """
        predictions = []
        for index, row in df_with_pred_ans.iterrows():
            if row['PredictedAnswer'].lower() in row['Sentence'].lower():
                predictions.append(1)
            else:
                predictions.append(0)

        return predictions



