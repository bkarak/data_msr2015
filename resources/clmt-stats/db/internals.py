
# global sqlalchemy objects
engine = None
base = None
Session = None


def get_base():
    return base


def create_database():
    base.metadata.create_all(engine)
