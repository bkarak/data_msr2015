import json
from conf.data_file import DataFile

from util.loggers import error


class Configuration(object):
    def __init__(self, config_filename):
        super(Configuration, self).__init__()
        try:
            self.__data_files = []
            fp = open(config_filename, 'r')
            self.__json_obj = json.load(fp)
            fp.close()

            for df_raw in self.__json_obj.get('data_files', []):
                df = DataFile(df_raw)

                if df.is_valid():
                    self.__data_files.append(df)
        except ValueError, ve:
            error("Configuration Error (Invalid JSON)")
            self.__json_obj = {}

    def get_data_files(self):
        return self.__data_files

    def get_plugins(self):
        return self.__json_obj.get('plugins', [])

    def get_data_directories(self):
        return self.__json_obj.get('data_directories', [])

    def get_database_url(self):
        return self.__json_obj.get('dburl', '')
