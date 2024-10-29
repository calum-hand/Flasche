import os

import pandas as pd

from flasche.db.manager import DB_MANAGER


def load_vocabulary():
    return pd.read_csv(DB_MANAGER.vocabulary_location)
