from urllib.request import urlopen
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, url):
        print(url)
        self.soup = BeautifulSoup(urlopen(url), 'html.parser')

class SearchResultScraper(Scraper):
    imdb_search_url = 'https://www.imdb.com/find?q={}'

    def __init__(self, serie_name):
        super().__init__(self.imdb_search_url.format(serie_name))

    def scrap_serie_IMDB_id(self):
        tag_first_result = self.soup.find('td', attrs={'class': 'result_text'})
        full_path = tag_first_result.find("a")['href']
        return full_path.split('/')[2]

    def scrap_serie_name(self):
        tag_first_result = self.soup.find('td', attrs={'class': 'result_text'})
        return tag_first_result.find("a").string

class SeasonScraper(Scraper):
    imdb_season_url = 'https://www.imdb.com/title/{}/episodes?season={}'

    def __init__(self, imdb_serie_id, season):
        super().__init__(self.imdb_season_url.format(imdb_serie_id, season))

    def scrap_serie_name(self):
        tag = self.soup.find('a', attrs={'itemprop': 'url'})
        return tag.string.strip()

    def scrap_season_number(self):
        tag = self.soup.find('h3', attrs={'id': 'episode_top'})
        season_name = tag.string.strip()
        splitted_season_name = season_name.split()
        return splitted_season_name[1]

    def scrap_season_year(self):
        tag = self.soup.find('div', attrs={'class': 'airdate'})
        first_epsode_date = tag.string.strip()
        splitted_first_epsode_date = first_epsode_date.split()

        try:
            return splitted_first_epsode_date[2]
        except IndexError as err:
             print("OS error: {0}".format(err))
             return None

    def scrap_epsodes(self):
        tag_all_epsodes = self.soup.find_all('div', attrs={'class': 'info'})

        epsodes = []
        for tag_epsode in tag_all_epsodes:
            epsode_number = tag_epsode.find("meta")['content']
            epsode_title = tag_epsode.find("strong").string

            epsodes.append((epsode_number, epsode_title))
        return epsodes
