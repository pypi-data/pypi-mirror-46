import pandas as pd
from omniscient.constants import *
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix

import logging
logging.basicConfig(level=logging.INFO)


def predict_from_file(model, input_file):
    df = pd.read_csv(input_file, sep=INPUT_FILE_SEPARATOR)

    # Add new 'context' column which combines all sentences relevant to a Question (to resemble a document)
    df['Context'] = pd.DataFrame(df.groupby(['QuestionID'])['Sentence'].transform(lambda x: ' '.join(x).lower()))

    # Create a new DataFrame with just the QuestionID, Question and the combined text. There will be duplicates equal
    # to the number of sentences - drop these as well
    df_contexts = df[['QuestionID', 'Question', 'Context']].drop_duplicates()

    # New DataFrame to hold QuestionID and the corresponding predicted answer
    df_qid_ans = pd.DataFrame(columns=['QuestionID', 'PredictedAnswer'])
    for index, row in df_contexts.iterrows():

        # NOTE: pred_ans is the snippet which has the answer, not the whole sentence
        pred_ans = predict_instance(model, row['Context'], row['Question'])[0]
        df_qid_ans = df_qid_ans.append({'QuestionID': row['QuestionID'], 'PredictedAnswer': pred_ans},
                                       ignore_index=True)
        logging.info("QuestionID: {} Question: {} Predicted Snippet: {}".
                     format(row['QuestionID'], row['Question'], pred_ans))

    df_with_pred_ans = pd.merge(df, df_qid_ans, on='QuestionID')

    # Check for match of answer snippet string with Sentence for each sentence so that each sentence can be labeled
    # as 0 or 1
    predictions = []
    for index, row in df_with_pred_ans.iterrows():
        if row['PredictedAnswer'][0].lower() in row['Sentence'].lower():
            predictions.append(1)
        else:
            predictions.append(0)

    df['PredictedLabel'] = predictions
    df.to_csv(PREDICTION_OUTPUT_DIR + "/" + PREDICTION_OUTPUT_FILE)

    logging.info("Precision, Recall, F-Score, Support: {}"
                 .format(precision_recall_fscore_support(df['Label'], df['PredictedLabel'])))
    logging.info("Confusion Matrix: {}".format(confusion_matrix(df['Label'], df['PredictedLabel'])))


def predict_instance(model, context, question):
    return model([context], [question])


