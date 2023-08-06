from unittest import TestCase
from deeppavlov import build_model, configs
import pytest


class TestModel(TestCase):
    def setUp(self):
        self.model = build_model(configs.squad.squad, download=True)

    def test_model_returns_correct_response_for_single_instance(self):
        ans = self.model(['DeepPavlov is library for NLP and dialog systems.'], ['What is DeepPavlov?'])[0][0]

        assert ans == 'library for NLP and dialog systems'
