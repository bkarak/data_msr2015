import json
import os
import sys
import urllib2


def download_maven(jar_name, full_url):
    print 'Downloading ... %s ... ' % (jar_name,),
    _url = urllib2.urlopen(full_url)
    _file = open('jars/%s' % (jar_name,), 'w')
    _file.write(_url.read())
    _file.close()
    print 'Done!'


def load_jars():
    result = {}
    fp = open('contrib/valid_jars.text', 'r')

    for line in fp:
        try:
            (header, filename) = line.split(':')
            result[os.path.basename(filename.strip())] = filename.strip().replace('/Users/bkarak/devel/repositories/maven/maven/', 'http://search.maven.org/remotecontent?filepath=')
        except Exception, e:
            print 'ERROR: %s' % (line,)

    fp.close()
    return result


def main():
    count = 0

    #valid_jars = load_jars()

    for item in os.listdir(sys.argv[1]):
        full_path = '%s%s' % (sys.argv[1], item)

        if full_path.endswith('-ckjm.json'):
            count += 1
            try:
                json.load(open(full_path, 'r'))
            except Exception, e:
                print item.replace('.jar-ckjm.json', '')
                valid_name = item.replace('-ckjm.json', '')
                #print valid_jars[valid_name]
                #download_maven(valid_name, valid_jars[valid_name])

    print '%d' % (count,)


if __name__ == '__main__':
    main()
