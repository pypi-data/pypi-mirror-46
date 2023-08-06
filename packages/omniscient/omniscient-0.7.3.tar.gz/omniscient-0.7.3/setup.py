from setuptools import setup, find_packages

REQUIRED_PACKAGES = [
    'scikit-learn',
    'pandas',
    'deeppavlov',
    'tensorflow',
    'flask'
]


setup(name='omniscient',
      version='0.7.3',
      description='Omniscient question answering system',
      long_description='Omniscient Question Answering System. Uses a BERT model fine-tuned on the SQuAD dataset.\
Returns predictions based on a Context and a Question. ',
      url='https://github.com/pasank/omniscient',
      author='Pasan Karunaratne',
      author_email='pasankarunaratne@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=REQUIRED_PACKAGES,
      zip_safe=False,
      )
