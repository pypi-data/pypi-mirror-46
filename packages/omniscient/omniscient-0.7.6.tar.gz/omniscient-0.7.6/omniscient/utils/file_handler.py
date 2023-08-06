import pandas as pd
from omniscient.utils.constants import *
import logging


class FileHandler:
    """
    Reading and writing CSV files to/from Pandas DataFrames
    """
    def __init__(self)->None:
        """
        Initialising FileHandler
        """
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Initialising FileReader")

    def read_dataframe_from_input_file(self, input_file: str)->pd.DataFrame:
        """
        Read raw DataFrame from input CSV file
        :param input_file: input CSV file
        :return: Pandas DataFrame correspodning to CSV file
        """
        try:
            logging.info("Reading dataframe from: {}".format(input_file))
            df = pd.read_csv(input_file, sep=INPUT_FILE_SEPARATOR)

            return df
        except IOError as e:
            raise

    def write_dataframe_to_output_file(self, df: pd.DataFrame, output_file: str)->None:
        """
        Write DataFrame to output CSV file
        :param df: input DataFrame (commonly one with the PredictedLabel column added)
        :param output_file: File to write out DataFrame to
        :return:
        """
        try:
            logging.info("Writing dataframe to: {}".format(output_file))
            df.to_csv(output_file)
        except IOError as e:
            raise