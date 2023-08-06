import pandas as pd


def predict_batch(model, input_file: str):
    df = pd.read_csv(input_file, sep='\t')

    # Add new 'context' column which combines all sentences relevant to a Question (to resemble a document)
    df['Context'] = pd.DataFrame(df.groupby(['QuestionID'])['Sentence'].transform(lambda x: ' '.join(x).lower()))

    # Create a new DataFrame with just the QuestionID, Question and the combined text. There will be duplicates equal
    # to the number of sentences - drop these as well
    df_contexts = df[['QuestionID', 'Question', 'Context']].drop_duplicates()

    # New DataFrame to hold QuestionID and the corresponding predicted answer
    df_qid_ans = pd.DataFrame(columns=['QuestionID', 'PredictedAnswer'])
    for index, row in df_contexts.iterrows():
        q = []
        d = []

        q.append(row['Question'])
        d.append(row['text'])

        q_id = row['QuestionID']
        pred_ans = predict_instance(model, d, q)[0]
        # pred_ans = model(d, q)[0]

        df_qid_ans = df_qid_ans.append({'QuestionID': q_id, 'PredictedAnswer': pred_ans}, ignore_index=True)
        print(q_id, row['Question'], pred_ans)

    df_with_pred_ans = pd.merge(df, df_qid_ans, on='QuestionID')

    predictions = []
    for index, row in df_with_pred_ans.iterrows():
        if row['PredictedAnswer'][0].lower() in row['Sentence'].lower():
            predictions.append(1)
        else:
            predictions.append(0)


def predict_instance(model, context, question):
    return model([context], [question])
