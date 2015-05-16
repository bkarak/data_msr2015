from sqlalchemy import or_
from util.data_structures import DictList
from db import models
from db.internals import Session

LINES_OF_CODE_CLMT = 18
CATEG_MODULE = 1
CATEG_CLASS = 2
CATEG_METHOD = 3
CATEG_CODE_UNIT = 4
CATEG_PROJECT_WIDE = [5, 6]


def __count_projects(db_session):
    return db_session.query(models.Project).count()


def __get_total_loc(db_session):
    _loc = 0

    for meas_obj in db_session.query(models.Measurement).filter(models.Measurement.mt_pk == LINES_OF_CODE_CLMT).filter(or_(models.Measurement.cat_pk == 5, models.Measurement.cat_pk == 6)):
        _loc += int(meas_obj.meas_value)

    return _loc


def __get_measurements(db_session):
    meas_list = DictList()

    for meas_obj in db_session.query(models.MeasurementType).all():
        __meas_arr = meas_obj.mt_name.split('_')
        meas_list.add(__meas_arr[0], __meas_arr[1], dup=False)

    return meas_list


def __get_measurements_ids(db_session):
    for meas_obj in db_session.query(models.MeasurementType).all():
        pass


def check_projects(db_session):
    total_projects = 0
    good_projects = 0

    for prj_obj in db_session.query(models.Project).all():
        for meas_obj in db_session.query(models.Measurement).filter(models.Project):
            pass


def __print_info(db_session):
    ckjm_metrics = 0
    clmt_metrics = 0
    jdepend_metrics = 0

    print 'Number of Projects: %d' % (__count_projects(db_session),)
    print 'Number of Classes: %d' % (0,)
    print 'LoC: %d' % (__get_total_loc(db_session),)
    print 'Measurements:'
    for (k, v) in __get_measurements(db_session).to_dict().iteritems():
        print '%s: %s' % (k, v)
        if 'ckjm' in v:
            ckjm_metrics += 1
        elif 'clmt' in v:
            clmt_metrics += 1
        elif 'jdepend' in v:
            jdepend_metrics += 1

    print 'Found ckjm: %d, clmt: %d, jdepend: %d' % (ckjm_metrics, clmt_metrics, jdepend_metrics)


def main():
    db_session = Session()
    __print_info(db_session)
    db_session.close()


if __name__ == '__main__':
    main()
