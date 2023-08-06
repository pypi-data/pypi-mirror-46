# coding=utf-8
import unittest

# noinspection PyUnresolvedReferences
import __init__
from hashtags import contains_hashtag, extract_hashtags


class TestHashtags(unittest.TestCase):

    def test_extract(self):
        assert (extract_hashtags("I love the #beach and #sand!") == {"#beach", "#sand"})

        assert (extract_hashtags(u"Pizza is so good! #~# 🍕") == set())

        assert (extract_hashtags("Man, Hashtags (#) are # nice # to # use # as # list # columns!") == set())

    def _disabled_test_unicode(self):  # Expect to fail this.
        # TODO add RTL unicode support to hashtag detection.
        assert (extract_hashtags(u"مرحبا# to the #world!") == {u'مرحبا#', '#world'})

    def test_simple_contains(self):
        assert (contains_hashtag('I enjoy #swimming!', 'swimming'))
        assert (contains_hashtag('I enjoy #swimming so much!', 'swimming'))

        assert (not (contains_hashtag("I dislike #coldswimming.", "#swimming")))
        assert (not (contains_hashtag("I dislike #coldswimming.", "#cold")))
        assert (contains_hashtag("I dislike #coldswimming.", "#coldswimming"))
