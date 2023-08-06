from flask import Flask, request
from omniscient.prediction.predictor import Predictor
import logging
from deeppavlov.core.common.chainer import Chainer
from omniscient.utils.constants import *


class RestEndpoint:
    """
    REST endpoint that enables question answering using an initialised model
    """

    def __init__(self, model: Chainer, host: str='0.0.0.0', port: int=5000)->None:
        """
        Initialises REST endpoint. Root will be a note on how to use the endpoint.
        /predict will be a POST endpoint which requires the specification of values for
         'context' and 'question' keys
        :param model: An initalised model
        :param host: Host address to run endpoint. NOTE '0.0.0.0' for externally visible server
        :param port: Port to run endpoint on
        """
        self.model = model
        self.predictor = Predictor(model)

        logging.info("Initialising REST endpoint using Flask")

        self.app = Flask(__name__)
        self.app.add_url_rule('/', 'index', self.index_action)
        self.app.add_url_rule('/predict', 'predict', self.predict_action, methods=['POST'])

        self.app.run(host=host, port=port)

    def predict_action(self)->str:
        """
        For the provided 'context' and 'question' in the /predict POST request, returns the
        matched snippet in the context.
        :return: Returns the matched snippet in the context for the question provided
        """
        data = request.get_json(force=True)

        context = data['context']
        question = data['question']

        logging.info("Received context: {}".format(context))
        logging.info("Received question: {}".format(question))

        matched_snippet = self.predictor.predict_instance(context, question)

        logging.info("Matched answer snippet: {}".format(matched_snippet))

        return matched_snippet

    def index_action(self)->str:
        """
        Returns a usage text
        :return: Text on how to use Omniscient REST endpoint for prediction
        """
        return "Omniscient Question Answering System. POST to /predict with 'context' and 'question' "
