from setuptools import setup

REQUIRED_PACKAGES = [
    'scikit-learn',
    'pandas',
    'deeppavlov',
    'tensorflow',
    'flask'
]


setup(name='omniscient',
      version='0.5',
      description='Omniscient question answering system',
      url='',
      author='Pasan Karunaratne',
      author_email='pasankarunaratne@gmail.com',
      license='MIT',
      packages=['omniscient'],
      install_requires=REQUIRED_PACKAGES,
      zip_safe=False,
      )
