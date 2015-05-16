import json, os

from parsers import jdepend
from util.loggers import warning, info


class DataFile(object):
    def __init__(self, data_file_json):
        super(DataFile, self).__init__()
        self.__data_file_json = data_file_json

    def filename(self):
        return self.__data_file_json.get('file', 'NotSet')

    def type(self):
        return self.__data_file_json.get('type', 'NotSet')

    def generator(self):
        return self.__data_file_json.get('generator', 'NotSet')

    def is_valid(self):
        __valid_gentypes = {'clmtx': ['json'], 'jdepend': ['xml']}
        generator_types = __valid_gentypes.get(self.generator(), None)

        if generator_types is None:
            warning('Invalid Generator %s not in %s' % (self.generator(), __valid_gentypes.keys()))
            return False

        if self.type() in generator_types:
            if os.path.exists(self.filename()):
                return True
            else:
                warning('File does not exist: %s' % (self.filename(),))
        else:
            warning('Invalid File Type %s not in %s' % (self.type(), generator_types))

        return False

    def load(self):
        results = []

        if self.is_valid():
            if self.generator() == 'clmtx':
                try:
                    fp = open(self.filename(), 'r')
                    data_json = json.load(fp)

                    for de in data_json:
                        # Artifact
                        results.append(None)

                    fp.close()
                except Exception, e:
                    warning('JSON is not in clmtx format (%s, %s)' % (self.filename(), e))
            elif self.generator() == 'jdepend':
                try:
                    data_json = jdepend.convert_jdepend_to_clmtx(self.filename())
                    for de in data_json:
                        # artifact
                        results.append(None)
                except Exception, e:
                    warning('XML is not in jdepend format (%s, %s)' % (self.filename(), e))

            info('Loading data ... %s (%s) ... %d artifacts' % (self.filename(), self.generator(), len(results)))

        return results

    def __str__(self):
        return 'filename: %s (%s, %s)' % (self.filename(), self.generator(), self.type())

    @staticmethod
    def load_directory(directory):
        if not os.path.exists(directory):
            warning('Directory does not exist (%s)' % (directory,))
            return []

        artifacts = []

        for (root, dirs, files) in os.walk(directory):
            for f in files:
                r = {'file' : '%s/%s' % (root, f)}

                if f.endswith('.json'):
                    r['type'] = 'json'
                    r['generator'] = 'clmtx'
                elif f.endswith('.xml'):
                    r['type'] = 'xml'
                    r['generator'] = 'jdepend'
                else:
                    continue

                artifacts.extend(DataFile(r).load())

        return artifacts




