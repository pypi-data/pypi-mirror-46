import json
import logging
import pandas as pd
from .preprocessor import PreProcessor
from .smalltalks import SmallTalks

class MessageCleaner:
    
    def __init__(self, data: list, config_file_path: str):
        self.data = pd.Series(data)
        self.preprocessor = PreProcessor()
        self.small_talks = SmallTalks()
        self.__set_config_information(config_file_path)
        self.__set_output_information()
        self.__set_logging_level()
        self.__use_placeholder = self.__config_information.get('use_placeholder', False)
        
    @classmethod
    def from_dataframe(cls, config_file_path: str, dataframe: pd.core.frame.DataFrame, content_column : str = 'Content'):
        return cls(dataframe[content_column].tolist(), config_file_path)
    
    @classmethod
    def from_series(cls, config_file_path: str, series: pd.core.frame.Series):
        return cls(series.tolist(), config_file_path)
    
    @classmethod
    def from_list(cls, config_file_path: str, lst: list):
        return cls(lst, config_file_path)
        
    @classmethod
    def from_file(cls, config_file_path: str, file_path : str, content_column : str = 'Content', encoding: str = 'utf-8', sep: str = ';'):
        dataframe = pd.read_csv(file_path, sep = sep, encoding = encoding, usecols = [content_column])
        dataframe.columns = ['Content']
        return cls(dataframe['Content'].tolist(), config_file_path)
    
    def clean(self):
        self.processed_df = pd.DataFrame({'Content': self.data, 'Processed Content': self.data.copy()})
        logging.info('Pre processing {} messages'.format(self.data.shape[0]))
        self.__remove_unimportant_data()
        self.preprocessor.set_data(self.processed_df['Processed Content'])
        self.processed_df['Processed Content'] = self.preprocessor.remove(self.__config_information, self.__use_placeholder)
        self.small_talks.set_data(self.processed_df['Processed Content'])
        result = self.small_talks.remove(self.__config_information, self.__use_placeholder)
        if result is not None:
            self.processed_df['Processed Content'] = result
        logging.info('Finished pre processing')
        self.__save_file()
        return self.processed_df
    
    def __set_config_information(self, config_file):
        try:
            with open(config_file, 'r') as f:
                self.__config_information = json.load(f)
        except:
            logging.error('Error reading json configuration file')
    
    def __set_logging_level(self):
        if self.__config_information.get('verbose', False):
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.WARNING)
            
    def __set_output_information(self):
        try:
            output_file = self.__config_information['output']
        except KeyError:
            self.__output_file_name = 'output_processed_content.csv'
            self.__output_file_encoding = 'utf-8'
            self.__output_file_sep = ';'
            self.__remove_duplicates = False
            self.__remove_empty = False
            self.__sort_by_length = False
            logging.warning('Missing output_file field. Setting default values to output variables.')
        else:
            self.__output_file_name = output_file.get('file_name', 'output_processed_content.csv')
            self.__output_file_encoding = output_file.get('file_encoding', 'utf-8')
            self.__output_file_sep = output_file.get('file_sep', ';')
            self.__remove_duplicates = output_file.get('remove_duplicates', False)
            self.__remove_empty = output_file.get('remove_empty', False)
            self.__sort_by_length = output_file.get('sort_by_length', False)
                   
    def __save_file(self):
        self.__remove_unimportant_data()
        if self.__sort_by_length:
            self.processed_df.index = self.processed_df['Processed Content'].str.len()
            self.processed_df = self.processed_df.sort_index(ascending=False).reset_index(drop=True)
        self.processed_df.to_csv(self.__output_file_name, sep= self.__output_file_sep , encoding= self.__output_file_encoding ,index= False)
    
    def __remove_unimportant_data(self):
        if self.__remove_empty:
            self.processed_df = self.processed_df.dropna().reset_index(drop=True)
        if self.__remove_duplicates:
            self.processed_df = self.processed_df.drop_duplicates(subset= ['Processed Content'], keep= 'first', inplace = False).reset_index(drop=True)