from db.internals import Session
from db.models import Project, Measurement


def __load_valid_projects():
    __v = []
    fp = open('contrib/projects.csv', 'r')
    for l in fp:
        __line = l.strip()
        __v.append(__line.split(';')[1])
    fp.close()

    return __v


def main():
    valid_projects = __load_valid_projects()
    db_session = Session()

    for project in db_session.query(Project).all():
        if project.prj_name not in valid_projects:
            rows_deleted = db_session.query(Measurement).filter(Measurement.prj_pk == project.prj_pk).delete()
            print 'Removed %s: %d' % (project.prj_name, rows_deleted)
            db_session.query(Project).filter(Project.prj_pk == project.prj_pk).delete()

    db_session.close()


if __name__ == '__main__':
    main()
