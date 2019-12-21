import pandas as pd
import requests
import gzip
import os
from db.operations import Operations
from util import create_logger

op = Operations()


class Preparations:
    def __init__(self):
        self.logger = create_logger(msg='Data Preparations')
        self.tv_series = op.get_imdb()
        self.columns = {
          'tconst': 'imdb_id',
          'primaryTitle': 'primary_title',
          'primaryTitle2': 'primary_title_lower',
                        }

    def get_imdb_data(self):
        """
        Get zipped title.basics file from datasets.imdbws

        :return: IMDB titles dataframe
        :rtype: pd.DataFrame
        """
        self.logger.info(msg='Getting IMDB Data')
        fname = 'title.basics.tsv.gz'
        url = 'https://datasets.imdbws.com/' + fname
        r = requests.get(url, stream=True)

        try:
            open(fname, 'wb').write(r.content)

            zipped = gzip.GzipFile(fname, 'rb')
            s = zipped.read()
            zipped.close()
            output = open("title.basics.tsv", 'wb')
            output.write(s)
            output.close()
            titles = pd.read_csv('title.basics.tsv', sep='\t')

        finally:
            os.remove("title.basics.tsv.gz")
            os.remove("title.basics.tsv")

        titles = titles[(titles['titleType'] == 'tvSeries') & (titles['startYear'] != '\\N')].reset_index(drop=True)
        titles['primaryTitle2'] = titles['primaryTitle'].apply(lambda x: x.lower())

        return titles[['tconst', 'primaryTitle', 'primaryTitle2']].rename(columns=self.columns)

    def merge_entries(self, name, season, episode):
        """
        Merge tv show list with IMDB titles data to get imdb_id.

        :param str name: Name of the TV show
        :param str season: Season of the TV show
        :param str episode: Episode of the TV show
        :return: TV shows dataframe with imdb_id
        :rtype: pd.DataFrame
        """
        self.logger.info('Merging Entries')

        imdb_id = self.tv_series[self.tv_series['primary_title_lower'] == name.lower()].imdb_id.values[0]
        name = self.tv_series[self.tv_series['primary_title_lower'] == name.lower()].primary_title.values[0]

        data = {
            'name': [name],
            'season': [season],
            'episode': [episode],
            'imdb_id': [imdb_id],
        }
        show_df = pd.DataFrame(data)

        return show_df
