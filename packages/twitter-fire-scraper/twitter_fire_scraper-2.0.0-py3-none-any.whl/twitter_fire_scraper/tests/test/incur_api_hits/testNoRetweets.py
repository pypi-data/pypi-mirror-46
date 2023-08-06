import unittest

from tests.test.incur_api_hits.cached_tweets import CachedTweets


class TestNoRetweets(unittest.TestCase):

    def testNoRetweets(self):
        """Tests that scraper can successfully scrape without retweets."""

        results = CachedTweets.tweets_medium_no_retweets()

        for term, statuses in results.items():
            for status in statuses:
                assert (status.retweeted == False)

                # Author of original tweet and person posting MUST be the same.
                # If not, it is a retweet.
                assert (status.author.id == status.user.id)
