import os, zipfile

def has_classes(filename):
    try:
        z = zipfile.ZipFile(filename)
        for f in z.namelist():
            if f.endswith('.class'):
                return True

        return False
    except Exception, e:
        print 'Error (has_classes()): %s' % (e,)
        return False

def get_jar_size(filename):
    size = 0
    
    if zipfile.is_zipfile(filename):
        try:
            z = zipfile.ZipFile(filename)
            for info in z.infolist():
                if info.filename.endswith('.class'):
                    size += info.file_size

            return size
        except Exception, e:
            print 'Error (get_jar_size()): %s' % (e,)
            return 0
    else:
        print 'BAD_FILE: %s is not a jar'
        return 0

def main():
    MAVEN_REPO = '/Users/bkarak/devel/repositories/maven/maven'

    for (root, dirs, files) in os.walk(MAVEN_REPO):
        for f in files:
            if f.endswith('.jar'):
                full_name = '%s/%s' % (root, f)
                print 'File: %s, has_classes: %s, size: %d' % (f, has_classes(full_name), get_jar_size(full_name))

if __name__ == '__main__':
    main()