# omniscient
Omniscient Question Answering System. Uses a BERT model fine-tuned on the SQuAD dataset.

Returns predictions based on a Context and a Question. 

E.g. 

_Context_: 'I have a dozen bananas. Not all of them are ripe.'

_Question_: 'How many bananas do I have?'

_Prediction_: In instance level question answering mode returns '_dozen_', 
in batch mode returns the sentence which contains the answer 
(_'I have a dozen bananas'_)


Can be used in batch mode for multiple predictions from a file, or 
deployed as a REST endpoint for instance level question answering. 

# Installation
```
pip install omniscient
```

# Usage

## Local Predictor
```
>>> import omniscient as omn
>>> mdl = omn.init_model()
>>> pr = omn.Predictor(mdl)
>>> pr.predict_instance('I have six bananas', 'How many bananas do I have')
>>> pr.predict_from_file('/data/omn_input.tsv', '/data/omn_output.tsv', fh)
```


## Deployed Predictor
```
>>> import omniscient as omn
>>> mdl = omn.init_model()
>>> init_endpoint(mdl)
```

