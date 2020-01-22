from bs4 import BeautifulSoup
from urllib.request import urlopen
from util import create_logger


class Crawler:
    BASE_PATH = 'https://www.imdb.com'

    def __init__(self):
        self.logger = create_logger(msg='Crawler')
        self.message = ''

    def crawl_airtimes(self, df):
        """
        Crawl airtimes of tv shows

        :param pd.DataFrame df: tv shows dataframe
        :return: e-mail text content
        :rtype: str
        """
        self.logger.info('Crawling Airtimes')

        for i in df.itertuples():
            imdb_id = i.imdb_id
            season = f'season={i.season}'
            url = f'{self.BASE_PATH}/title/{imdb_id}'
            html = urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            p1 = soup.find('div', attrs={'class': 'seasons-and-year-nav'})
            p2 = p1.findAll('a')

            href = [link.get('href') for link in p2]
            season_url = [k for k in href if season in k]

            try:
                season_url = f'{self.BASE_PATH}{season_url[0]}'
                html = urlopen(season_url)
                soup2 = BeautifulSoup(html, 'html.parser')

                # Find episode by its number
                episode = i.episode
                d = soup2.find('meta', attrs={'itemprop': 'episodeNumber', 'content': episode})
                text = d.findNext('div').text
                text = text.strip()

                if len(text) > 2:
                    check = f'Airing time for season {i.season}, episode {episode} of {i.name} is {text}'
                else:
                    check = f'Airing time for season {i.season}, episode {episode} of {i.name} is not anounced yet'
            except:
                check = f'Airing time for season {i.season}, episode {episode} of {i.name} is not anounced yet'
            self.message = self.message + '\n' + check

        return self.message
