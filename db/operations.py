from db import connect
from db.tv_series import TvSeries
from db.imdb_dataset import ImdbDataset
import pandas as pd
from util import create_logger


ts = TvSeries
imdb = ImdbDataset


class Operations:
    def __init__(self):
        self.logger = create_logger(msg='Database Operations')

    def insert(self, df, table='tv_series', method='append'):
        """

        :param df:
        :param table:
        :param method:
        :return:
        """
        self.logger.info('Inserting tv_series to db')

        session = connect()

        args = {
            'name': table,
            'con': session.bind,
            'if_exists': method,
            'index': False,
        }
        try:
            df.to_sql(**args)
        finally:
            session.close()

    def get_imdb(self):
        """

        :return:
        """
        self.logger.info('Get dataframe from db')

        session = connect()

        cols = [
            imdb.imdb_id,
            imdb.primary_title,
            imdb.primary_title_lower,
        ]

        query = session.query(*cols) \
            .select_from(imdb)

        try:
            return pd.read_sql(query.statement, session.bind)
        finally:
            session.close()

    def get_dataframe(self):
        """

        :return:
        """
        self.logger.info('Get dataframe from db')

        session = connect()

        cols = [
            ts.imdb_id,
            ts.name,
            ts.season,
            ts.episode,
        ]

        query = session.query(*cols) \
            .select_from(ts)

        try:
            return pd.read_sql(query.statement, session.bind)
        finally:
            session.close()

    def get_list(self):
        """
        Get TV shows list

        :return: TV show list rows
        :rtype: list
        """
        self.logger.info('Get Results')

        session = connect()

        try:
            return session.query(ts).all()

        finally:
            session.close()

    def get_by_id(self, imdb_id):
        """
        Get by primary key

        :param str imdb_id: Tv series IMDB id
        :return: Tv series entity
        :rtype: TvSeries
        """
        session = connect()

        try:
            return session.query(ts).filter(ts.imdb_id == imdb_id).first()
        finally:
            session.close()

    def delete_by_id(self, imdb_id):
        """
        Delete record by IMDB id

        :param str imdb_id: IMDB id
        """
        self.logger.info('Deleting record from database')
        session = connect()

        try:
            session.query(ts).filter(ts.imdb_id == imdb_id).delete()
            session.commit()
        finally:
            session.close()

    def update(self, record):
        """
        Insert new season and episode numbers

        :param TvSeries record: Tv series entity
        """
        self.logger.info('Update record from database')
        session = connect()

        try:
            session.merge(record)
            session.commit()
        finally:
            session.flush()
            session.close()
