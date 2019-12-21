from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def connect():
    """
    :return: database session
    :rtype: sqlalchemy.orm.session.Session
    """
    conn_args = {'check_same_thread': False}
    engine = create_engine('sqlite:///airtime.db', connect_args=conn_args)
    return sessionmaker(bind=engine)()
