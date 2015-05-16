from sqlalchemy import Column, Integer, String, ForeignKey
from db.internals import base
from util.loggers import info

caching = {}


class Project(base):
    __tablename__ = 'project'

    prj_pk = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    prj_name = Column(String(500), nullable=False, index=True)

    @staticmethod
    def get_or_insert(project_name):
        if project_name in caching:
            return caching[project_name]

        from db.internals import Session

        if len(project_name.strip()) == 0:
            return -1

        _result = None
        _db_session = Session()

        try:
            _result = _db_session.query(Project).filter(Project.prj_name == project_name).one()
            _result = _result.prj_pk
        except Exception, e:
            _project_object = Project()
            _project_object.prj_name = project_name
            _db_session.add(_project_object)
            _db_session.commit()
            info('Adding Project %s with id: %d' % (project_name, _project_object.prj_pk))
            _result = _project_object.prj_pk

        _db_session.close()
        caching[project_name] = _result

        return _result


class Category(base):
    __tablename__ = 'category'

    cat_pk = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    cat_name = Column(String(500), nullable=False, index=True)

    @staticmethod
    def get_or_insert(category_name):
        if category_name in caching:
            return caching[category_name]

        from db.internals import Session

        if len(category_name.strip()) == 0:
            return -1

        _result = None
        _db_session = Session()

        try:
            _result = _db_session.query(Category).filter(Category.cat_name == category_name).one()
            _result = _result.cat_pk
        except Exception, e:
            category_object = Category()
            category_object.cat_name = category_name
            _db_session.add(category_object)
            _db_session.commit()
            info('Adding Category %s with id: %d' % (category_name, category_object.cat_pk))
            _result = category_object.cat_pk

        _db_session.close()

        caching[category_name] = _result

        return _result


class Filenames(base):
    __tablename__ = 'filenames'

    fl_pk = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    fl_name = Column(String(500), nullable=False, index=True)

    @staticmethod
    def get_or_insert(fl_name):


        from db.internals import Session

        if len(fl_name.strip()) == 0:
            fl_name = 'project-wide'

        _result = None
        _db_session = Session()

        try:
            _result = _db_session.query(Filenames).filter(Filenames.fl_name == fl_name).one()
            _result = _result.fl_pk
        except Exception, e:
            fl_object = Filenames()
            fl_object.fl_name = fl_name
            _db_session.add(fl_object)
            _db_session.commit()
            #info('Adding Filename/Id %s with id: %d' % (fl_name, fl_object.fl_pk))
            _result = fl_object.fl_pk

        _db_session.close()

        return _result


class MeasurementType(base):
    __tablename__ = 'measurement_type'

    mt_pk = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    mt_name = Column(String(500), nullable=False, index=True)

    @staticmethod
    def get_or_insert(mtype_name):
        if mtype_name in caching:
            return caching[mtype_name]

        from db.internals import Session

        if len(mtype_name.strip()) == 0:
            return -1

        _result = None
        _db_session = Session()

        try:
            _result = _db_session.query(MeasurementType).filter(MeasurementType.mt_name == mtype_name).one()
            _result = _result.mt_pk
        except Exception, e:
            mt_object = MeasurementType()
            mt_object.mt_name = mtype_name
            _db_session.add(mt_object)
            _db_session.commit()
            info('Adding Measurement Type %s with id: %d' % (mtype_name, mt_object.mt_pk))
            _result = mt_object.mt_pk

        _db_session.close()

        caching[mtype_name] = _result

        return _result


class Measurement(base):
    __tablename__ = 'measurement'

    meas_pk = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    meas_value = Column(String(500), nullable=False)
    meas_id = Column(Integer, ForeignKey('filenames.fl_pk'), nullable=False)
    meas_filename = Column(Integer, ForeignKey('filenames.fl_pk'), nullable=False)
    cat_pk = Column(Integer, ForeignKey('category.cat_pk'), nullable=False)
    prj_pk = Column(Integer, ForeignKey('project.prj_pk'), nullable=False)
    mt_pk = Column(Integer, ForeignKey('measurement_type.mt_pk'), nullable=False)

