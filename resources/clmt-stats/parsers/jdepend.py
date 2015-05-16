from parsers import xmldict
from util.loggers import warning


def convert_jdepend_to_clmtx(filename):
    result = []

    try:
        fp = open(filename, 'r')
        xml_json = xmldict.parse(fp)
        packages = xml_json['JDepend']['Packages']['Package']

        if isinstance(packages, list):
            for p in packages:
                try:
                    package_name = p.get('@name', 'NotSet')

                    if p.get('error', None) is not None:
                        continue

                    stats = p.get('Stats', {})
                    results = {'id': package_name,
                               'filename': package_name.replace('.', '/'),
                               'category': 'module',
                               'measurement': [
                                   {'name': 'NumberOfClasses', 'result-type': 'integer', 'value': stats.get('TotalClasses', 0)},
                                   {'name': 'NumberOfConcreteClasses', 'result-type': 'integer', 'value': stats.get('ConcreteClasses', 0)},
                                   {'name': 'NumberOfAbstractClasses', 'result-type': 'integer', 'value': stats.get('AbstractClasses', 0)},
                                   {'name': 'AfferentCouplings', 'result-type': 'integer', 'value': stats.get('Ca', 0)},
                                   {'name': 'EfferentCouplings', 'result-type': 'integer', 'value': stats.get('Ce', 0)},
                                   {'name': 'Abstractness', 'result-type': 'float', 'value': stats.get('A', 0.0)},
                                   {'name': 'Instability', 'result-type': 'float', 'value': stats.get('I', 0.0)},
                                   {'name': 'DistanceMainSequence', 'result-type': 'float', 'value': stats.get('D', 0.0)}]}
                    result.append(results)
                except Exception, e:
                    warning('Conversion error: %s' % (e,))
                    continue
    except Exception, e:
        warning('Could not convert JDepend XML to clmtx (%s, %s)' % (filename, e))

    return result
