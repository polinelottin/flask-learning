from models.serie import SerieModel
from models.season import SeasonModel
from models.epsode import EpsodeModel

from scraping.scraper import SearchResultScraper, SeasonScraper

class ScrapController:

    @classmethod
    def scrap_serie_and_save_to_db(cls, serie_name_request):
        controller = cls()
        serie = controller.find_serie_or_create(serie_name_request)

        controller.browse_seasons_and_import(serie)

        return serie

    def browse_seasons_and_import(self, serie):
        season_number = 1
        while(True):
            print('start importing season {}...'.format(season_number))

            season_scraper = SeasonScraper(serie.IMDB_id, season_number)
            scraped_season_number = int(season_scraper.scrap_season_number())

            if scraped_season_number == season_number:
                season = self.find_season_or_create(serie, scraped_season_number, season_scraper)
                self.import_epsodes(serie, season, season_scraper)
                season_number += 1
            else:
                break

    def import_epsodes(self, serie, season, season_scraper):
        epsodes = season_scraper.scrap_epsodes()

        for epsode_data in epsodes:
            epsode = EpsodeModel.find_by_serie_id_and_season_id_and_number(serie.id, season.id, epsode_data[0])

            if not epsode:
                print("importing epsode S{} Ep{} - {}".format(season.id, epsode_data[0], epsode_data[1]))
                epsode = EpsodeModel(serie.id, season.id, epsode_data[0], epsode_data[1])
                epsode.save_to_db()

        print('success!')

    def find_season_or_create(self, serie, season_number, season_scraper):
        season = SeasonModel.find_by_serie_id_and_number(serie.id, season_number)

        if not season:
            season_year = season_scraper.scrap_season_year()

            print('importing season {} year {}'.format(season_number, season_year))
            season = SeasonModel(serie.id, season_number, season_year)
            season.save_to_db()

            season = SeasonModel.find_by_serie_id_and_number(serie.id, season_number)

        return season

    def find_serie_or_create(self, serie_name_request):
        serie_scraper = SearchResultScraper(serie_name_request)

        serie_IMDB_name = serie_scraper.scrap_serie_name()
        serie = SerieModel.find_by_name(serie_IMDB_name)

        if not serie:
            serie_IMDB_id = serie_scraper.scrap_serie_IMDB_id()

            print('importing serie {} id {}'.format(serie_IMDB_name, serie_IMDB_id))
            serie = SerieModel(serie_IMDB_name, serie_IMDB_id)
            serie.save_to_db()

            serie = SerieModel.find_by_name(serie_IMDB_name)

        return serie
