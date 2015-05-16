from Queue import Queue
import json
import sys
import os
import re
from threading import Thread
import db.internals

from parsers.clmt_xml import convert_clmtx_to_clmt_json
from parsers.jdepend import convert_jdepend_to_clmtx

from db.project_status import ProjectStatus

from util.loggers import error, info, warning

sanity_checks = {}


def infer_project_name(filename):
    project_name = filename
    project_input = None

    if filename.endswith('.jar-ckjm.json'):
        project_name = project_name.replace('.jar-ckjm.json', '')
        project_input = 'ckjm'
    elif filename.endswith('.jar-jdepend.xml'):
        project_name = project_name.replace('.jar-jdepend.xml', '')
        project_input = 'jdepend'
    elif filename.endswith('-sources.jar-clmt.xml'):
        project_name = project_name.replace('-sources.jar-clmt.xml', '')
        project_input = 'clmt'
    else:
        raise Exception('Invalid project name')

    mobj = re.match('(.*)-[0-9]+\\.[0-9]+.*', project_name)

    if mobj is not None:
        project_name = mobj.group(1).strip()

    return project_name, project_input


def import_file(filename):
    try:
        if not filename.endswith('.xml') and not filename.endswith('.json'):
            raise Exception('Accepting only (.json, .xml) formats: %s' % (filename,))

        json_obj = None

        if filename.endswith('-jdepend.xml'):
            json_obj = convert_jdepend_to_clmtx(filename)

        if filename.endswith('-clmt.xml'):
            json_obj = convert_clmtx_to_clmt_json(filename)

        if json_obj is None:
            fp = open(filename, 'r')
            json_obj = json.load(fp)
            fp.close()

        (project_name, project_input) = infer_project_name(filename)
        project_status = sanity_checks.get(project_name, ProjectStatus(project_name))

        if project_input == 'jdepend':
            project_status.jdepend_imported = True
        elif project_input == 'clmt':
            project_status.clmt_imported = True
        elif project_input == 'ckjm':
            project_status.ckjm_imported = True

        project_name = os.path.basename(project_name)

        sanity_checks[project_name] = project_status
        import_json(project_name, project_input, json_obj)
    except Exception, e:
        error('Could not import %s (%s)' % (filename, e))


def import_json(project_name, project_input, json_obj):
    from db.models import Filenames, Category, Project, Measurement, MeasurementType

    info('Importing Project: %s (%s)' % (project_name, project_input))
    _project_obj = Project.get_or_insert(project_name)

    if _project_obj == -1:
        error('Could not import Project: %s (%s)' % (project_name, project_input))
        return

    for element in json_obj:
        try:
            # retrieve id
            _id = element['id']
            _category = element['category']
            _filename = element['filename']

            # retrieve ids
            _id_obj = Filenames.get_or_insert(_id)

            if _id_obj == -1:
                warning('Invalid Element (id, filename): (%s, %s)' % (_id, _filename))
                continue

            # retrieve categories
            _category_obj = Category.get_or_insert(_category)

            if _category_obj == -1:
                warning('Invalid Element (id, filename): (%s, %s)' % (_id, _filename))
                continue

            # retrieve filenames
            _filename_obj = Filenames.get_or_insert(_filename)

            if _filename_obj == -1:
                warning('Invalid Element (id, filename): (%s, %s)' % (_id, _filename))
                continue

            from db.internals import Session

            db_session = Session()

            for measurements in element.get('measurement', []):
                try:
                    try:
                        _name = measurements[u'name']
                    except Exception, e:
                        _name = measurements[u'Name']

                    _mt_obj = MeasurementType.get_or_insert(_name + '_' + project_input)

                    if _mt_obj == -1:
                        warning('Invalid Measurement Type: %s' % (_name + '_' + project_input,))
                        continue

                    _value = str(measurements['value'])

                    meas_object = Measurement()
                    meas_object.cat_pk = _category_obj
                    meas_object.prj_pk = _project_obj
                    meas_object.meas_id = _id_obj
                    meas_object.meas_filename = _filename_obj
                    meas_object.meas_value = _value
                    meas_object.mt_pk = _mt_obj
                    db_session.add(meas_object)
                except Exception, e:
                    warning('Invalid Measurement: %s (%s)' % (measurements, e.message))
                    continue

            db_session.commit()
            db_session.close()
        except Exception, e:
            error('%s (%s) - %s' % (project_name, project_input, e))


def import_directory(path):
    import subprocess

    q = Queue(maxsize=500)
    count = 0

    def do_work():
        while True:
            item = q.get(block=True)
            #import_file(item)
            print 'Working on %s' % (item,)
            subprocess.call(['python', 'clmt-stats.py', '-f', item])
            q.task_done()

    for i in range(4):
        t = Thread(target=do_work)
        t.daemon = True
        t.start()

    for filename in os.listdir(path):
        full_path = path + filename

        if os.path.isfile(full_path):
            q.put(full_path, block=True)
            count += 1
            print 'File Count: %d' % (count,)

    q.join()


def check_directory(path):
    from db.models import Project

    for filename in os.listdir(path):
        full_path = path + filename

        if os.path.isfile(full_path):
            try:
                (project_name, project_input) = infer_project_name(filename)
                project_name = os.path.basename(project_name)

                Project.get_or_insert(project_name)

                project_status = sanity_checks.get(project_name, ProjectStatus(project_name))

                if project_input == 'jdepend':
                    project_status.jdepend_imported = True
                elif project_input == 'clmt':
                    project_status.clmt_imported = True
                elif project_input == 'ckjm':
                    project_status.ckjm_imported = True

                sanity_checks[project_name] = project_status
            except Exception, e:
                print '%s' % (full_path,)


def main():
    info("CLMT Data Processing Tool")
    info("-------------------------")
    info("Vassilios Karakoidas (c) 2013")
    info("vassilios.karakoidas@gmail.com (http://bkarak.wizhut.com/)")
    info("")

    if len(sys.argv) not in [1, 2, 3]:
        error('usage: clmt-stats.py [initdb|-d {directory}|-f {file}]')
        return

    if sys.argv[1] == 'initdb':
        from db.internals import create_database

        info("Creating the SQLite database ... ")
        create_database()
        return

    if len(sys.argv) == 3:
        if sys.argv[1] == '-f' and os.path.isfile(sys.argv[2]):
            info('Checking file: %s' % (sys.argv[2],))
            import_file(sys.argv[2])
        elif sys.argv[1] == '-d' and os.path.isdir(sys.argv[2]):
            info('Checking directory: %s' % (sys.argv[2],))
            import_directory(sys.argv[2])
        elif sys.argv[1] == '-dups' and os.path.isdir(sys.argv[2]):
            info('Duplicates Check on %s' % (sys.argv[2],))
            check_directory(sys.argv[2])
        else:
            warning('"%s" is not a valid file to import!' % (sys.argv,))

if __name__ == '__main__':
    main()

