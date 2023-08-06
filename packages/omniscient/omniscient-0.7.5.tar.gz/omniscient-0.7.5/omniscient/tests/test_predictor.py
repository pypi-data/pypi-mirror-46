from unittest import TestCase
from deeppavlov import build_model, configs
from omniscient.prediction.predictor import Predictor
import pandas as pd


class TestModel(TestCase):
    def setUp(self):
        self.model = build_model(configs.squad.squad, download=True)
        self.predictor = Predictor(self.model)

    def test_model_returns_correct_response_for_single_instance(self):
        ans = self.predictor.predict_instance('DeepPavlov is library for NLP and dialog systems.',
                                              'What is DeepPavlov?')

        assert ans == 'library for NLP and dialog systems'

    def test_model_returns_correct_response_for_batch(self):
        df = pd.DataFrame({'QuestionID': ['Q1', 'Q1', 'Q1', 'Q1', 'Q1'],
                           'Question': ['how are glacier caves formed?', 'how are glacier caves formed?',
                                        'how are glacier caves formed?', 'how are glacier caves formed?',
                                        'how are glacier caves formed?'],
                           'DocumentID': ['D1', 'D1', 'D1', 'D1', 'D1'],
                           'SentenceID': ['D1-0', 'D1-1', 'D1-2', 'D1-3', 'D1-4'],
                           'Sentence': ['A partly submerged glacier cave on Perito Moreno Glacier .',
                                        'The ice facade is approximately 60 m high',
                                        'Ice formations in the Titlis glacier cave',
                                        'A glacier cave is a cave formed within the ice of a glacier .',
                                        'Glacier caves are often called ice caves , but this term is properly used to '
                                        'describe bedrock caves that contain year-round ice.'],
                           'Label': [0, 0, 0, 1,0 ]
                           })
        df_ans = self.predictor.predict_batch(df)

        ans = df_ans[df_ans['PredictedLabel'] == 1]['Sentence'].tolist()[0]

        assert ans == 'A glacier cave is a cave formed within the ice of a glacier .'
