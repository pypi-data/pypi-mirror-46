from tweet_model.tweet import Tweet
from tweet_model import utils

import pytest
import os
import datetime


#################
#   FIXTURES    #
#################
@pytest.fixture
def empty_tweet():
    return Tweet()


@pytest.fixture
def tweet1():
    return Tweet(id="128977963458933",
                 text="En un lugar de la Mancha...",
                 user__name="Julio César",
                 user__created_at="2019-05-01 23:54:27")


@pytest.fixture
def dict_tweet1():
    dictionary_tweet1 = {}
    dictionary_tweet1["id"] = 128977963458933
    dictionary_tweet1["text"] = "En un lugar de la Mancha..."
    dictionary_tweet1["user"] = {}
    dictionary_tweet1["user"]["name"] = "Julio César"
    dictionary_tweet1["user"]["created_at"] =\
        datetime.datetime(2019, 5, 1, 23, 54, 27)

    return dictionary_tweet1


@pytest.fixture
def csv_file_path():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, "resources", "01.csv")


@pytest.fixture
def fake_file_path():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, "resources", "false.csv")


##############
#   TESTS    #
##############
class TestTweetObjects:
    def test_empty_tweet_instantiation__OK(self, empty_tweet):
        """
        Check that a Tweet object can be instantiated with no values and
        then all its not-nested attributes will be None (or False, since Nones
        can be casted to boolean as False)
        """

        for key, value in empty_tweet.__dict__.items():
            if type(value) is not dict:
                assert value in (None, False)

    def test_nonempty_tweet_instantiation__values_OK(self, tweet1):
        """
        Check some of the nested and non-nested fields after instantiating a
        Tweet with some initial valid values
        """

        assert tweet1.id == 128977963458933
        assert tweet1.text == "En un lugar de la Mancha..."
        assert tweet1["user"]["name"] == "Julio César"
        assert tweet1["user"]["created_at"] ==\
            datetime.datetime(2019, 5, 1, 23, 54, 27)
        assert tweet1["coordinates"]["coordinates"] is None

    def test_nonempty_tweet_instantiation__typing_OK(self, tweet1):
        """
        Check some of the nested and non-nested fields have the right typing
        """

        assert type(tweet1.id) == int
        assert type(tweet1.text) == str
        assert type(tweet1["user"]["name"]) == str
        assert type(tweet1["user"]["created_at"]) == datetime.datetime
        assert isinstance(tweet1["coordinates"]["coordinates"], type(None))

    def test_get_tweet_fields_subset_OK(self, tweet1):
        """
        Check that the "as_json" function returns a correct JSON representation
        of the Tweet object
        """

        new_dict = tweet1.get_tweet_fields_subset(["id", "text"])
        assert new_dict == {"id": 128977963458933,
                            "text": "En un lugar de la Mancha..."}


class TestTweetUtils:
    def test_get_tweet_from_csv_raw_line_OK(self, csv_file_path):
        """
        Check that a Tweet object can be instantiated from a CSV file that
        contains at least a header in the 1st line indicating the names of the
        fields and a tweet description in the 2nd with a value for each of that
        fields.
        """

        with open(csv_file_path) as file_reader:
            header = file_reader.readline()
            tweet_contents = file_reader.readline()
        tweet = utils.get_tweet_from_csv_raw_line(header, tweet_contents)

        assert tweet["id"] == 1123738691938193410

    def test_get_tweets_from_csv_OK(self, csv_file_path):
        """
        Check that all the tweets from a CSV file can be instantiated at once
        using the function "get_tweets_from_csv". Check the length of the list
        so it matches the lines in the CSV and check some ids of the
        instantiated tweets
        """

        tweets = utils.get_tweets_from_csv(csv_file_path)

        assert len(tweets) == 3214
        assert tweets[3213]["id"] == 1123376500898783238

    def test_get_tweets_from_csv_ERROR(self, fake_file_path):
        """
        Check that, if provided with a file that doesn't correspond to a tweet
        specification, an appropriate exception is raised
        """

        with pytest.raises(utils.NotValidTweetError):
            utils.get_tweets_from_csv(fake_file_path)
