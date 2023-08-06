import json
import os

class Config:
    DEFAULT_MONGODB_CONNECTION_STRING = "mongodb://localhost:27017/"

def try_get(object, key):
    """Tries to get the value of a key in an object, and politely notifies you if it cannot find it."""

    if key not in object:
        raise KeyError("Could not find " + key + " inside of " + object + "! Does it exist?")

    return object[key]


class DataConfig:
    """Holds data and filepath configuration information for data files such as state names, hashtags we wish to track,
    terms that indicate fires or disasters, etc."""

    # Folder name that data is stored in.
    DATA_FOLDER_NAME = "data"

    # Path data is stored in.
    DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), DATA_FOLDER_NAME)

    # Disaster hashtag datafile location.
    DISASTER_HASHTAGS_DATA_PATH = os.path.join(DATA_PATH, "DisasterHashtags.yml")

    # Fire hashtag datafile location.
    FIRE_HASHTAGS_DATA_PATH = os.path.join(DATA_PATH, "FireHashtags.yml")

    # US major cities datafile location.
    MAJOR_CITIES_DATA_PATH = os.path.join(DATA_PATH, "MajorCities.yml")

    # US states datafile location.
    US_STATES_DATA_PATH = os.path.join(DATA_PATH, "USStates.yml")

    TWITTER_ACCOUNTS_DATA_PATH=os.path.join(DATA_PATH, "TwitterAccounts.yml")
