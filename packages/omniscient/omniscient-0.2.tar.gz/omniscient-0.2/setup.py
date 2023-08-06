from setuptools import setup
from setuptools.command.install import install
from subprocess import check_call


REQUIRED_PACKAGES = [
    'scikit-learn',
    'pandas',
    'deeppavlov',
    'tensorflow'
]


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # check_call("python -m deeppavlov download deeppavlov/configs/squad/squad_bert.json".split())
        from deeppavlov import build_model, configs
        model = build_model(configs.squad.squad_bert, download=True)

        install.run(self)


setup(name='omniscient',
      version='0.2',
      description='Omniscient question answering system',
      url='',
      author='Pasan Karunaratne',
      author_email='pasankarunaratne@gmail.com',
      license='MIT',
      packages=['omniscient'],
      install_requires=REQUIRED_PACKAGES,
      zip_safe=False,
      # cmdclass={
      #     'install': PostInstallCommand,
      # }
      )
