from deeppavlov import build_model, configs
from omniscient.predictor import predict_from_file, predict_instance
from omniscient.constants import *
from flask import Flask, request, jsonify

import logging
logging.basicConfig(level=logging.INFO)


def predict_batch(model, file_name):
    return predict_from_file(model, file_name)


def init():
    global model

    logging.info("Initialising SQuAD model...")
    model = build_model(configs.squad.squad, download=True)

    logging.info("Predicting on one example to test...")
    ans = model(['DeepPavlov is library for NLP and dialog systems.'], ['What is DeepPavlov?'])

    logging.info("Test example answer: {}".format(ans[0][0]))

    if IS_ENABLE_PREDICTION_ENDPOINT:
        app.run()


app = Flask(__name__)


@app.route('/')
def home():
    return "Omniscient Question Answering System"


@app.route('/predict', methods=['POST'])
def handle_predict_request():
    data = request.get_json(force=True)

    context = data['context']
    question = data['question']

    logging.info("Received context: {}".format(context))
    logging.info("Received question: {}".format(context))

    model_response = predict_instance(model, context, question)
    matched_snippet = model_response[0][0]

    logging.info("Model response: {}".format(model_response))
    logging.info("Matched answer snippet: {}".format(matched_snippet))

    return model_response[0][0]


if __name__ == '__main__':
    init()
