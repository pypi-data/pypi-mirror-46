from deeppavlov import build_model, configs
from omniscient.endpoint.rest_endpoint import RestEndpoint
from deeppavlov.core.common.chainer import Chainer
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def init_model()->Chainer:
    """
    Initialises model. Downloads pretrained weights if necessary (hash check conducted before download)
    :return: The initialised model that can be passed to a Predictor object
    """
    logging.info("Initialising SQuAD model")
    model = build_model(configs.squad.squad, download=True)

    return model


def init_endpoint(model: Chainer, host: str='0.0.0.0', port: int=5000):
    """
    Initialises an REST endpoint to query for predictions
    :param model: The model initialised via init_model()
    :param host: Host address to run endpoint. NOTE '0.0.0.0' for externally visible server
    :param port: Port to run endpoint on
    :return: The initialised REST endpoint
    """
    restendpoint = RestEndpoint(model, host, port)


if __name__ == '__main__':
    # If run as main will initialise model and an endpoint that uses that model to provide predictions
    mdl = init_model()
    init_endpoint(mdl)
