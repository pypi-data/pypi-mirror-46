import unittest

from twitter_fire_scraper.scraper import Scraper
from twitter_fire_scraper.twitter import TwitterAuthentication
from pymongo import MongoClient

from util import get_status_text


class TestSimpleScraping(unittest.TestCase):

    def testCanScrapeTerm(self):
        """Tests that scraper can scrape one term."""

        twauth = TwitterAuthentication.autodetect_twitter_auth()

        scraper = Scraper(twitter_authentication=twauth)

        results = scraper.scrape_terms({"fire"}, count=1)

        assert('fire' in results)

        assert(isinstance(results['fire'], list))

        assert (len(results.keys()) == 1)

        assert (isinstance(get_status_text(results['fire'][0]), str))

    def testCanScrapeAccount(self):
        """Tests that scraper can scrape one account."""
        twauth = TwitterAuthentication.autodetect_twitter_auth()

        scraper = Scraper(twitter_authentication=twauth)

        results = scraper.scrape_accounts({"@RedCross"}, count=1)

        assert ('@RedCross' in results)

        assert (len(results.keys()) == 1)

        assert(isinstance(results['@RedCross'], list))

        assert (isinstance(get_status_text(results['@RedCross'][0]), str))

    def testCanScrapeMethod(self):
        """Tests that the Scraper's `scrape` method works."""

        twauth = TwitterAuthentication.autodetect_twitter_auth()

        scraper = Scraper(twitter_authentication=twauth)

        results = scraper.scrape(terms={"fire"}, accounts={"@RedCross"})

        assert('fire' in results.keys())
        assert('@RedCross' in results.keys())

        assert(len(results.keys()) == 2)

        assert(isinstance(results['fire'], list))
        assert(isinstance(results['@RedCross'], list))

    def testCanScrapeAndSave(self):
        """Tests if the Scraper can both scrape and save the results to a MongoDB database"""

        # Before starting, if the test database exists, remove it
        # TODO: standardize localhost string
        test_client = MongoClient()
        test_db = "testdb"
        test_client.drop_database(test_db)

        twauth = TwitterAuthentication.autodetect_twitter_auth()

        scraper = Scraper(twitter_authentication=twauth)

        results = scraper.scrape_and_save(terms={"fire"}, count=1, dbname="testdb")

        assert ('fire' in results.keys())

        assert (len(results.keys()) == 1)

        assert (isinstance(results['fire'], list))

        assert (test_client[test_db].get_collection("fire").count() == 1)
        test_client.drop_database(test_db)

    def _disabled_testLotsOfTweets(self):
        """Tests if the Scraper can retrieve 1000 tweets for one term"""
        twauth = TwitterAuthentication.autodetect_twitter_auth()

        scraper = Scraper(twitter_authentication=twauth)

        results = scraper.scrape(terms={"fire"}, count=1000)

        assert ('fire' in results.keys())

        assert (len(results.keys()) == 1)

        assert (isinstance(results['fire'], list))

        assert (len(results['fire']) == 1000)

