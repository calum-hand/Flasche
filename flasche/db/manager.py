import os
from enum import Enum
from dataclasses import dataclass

from flasche.config import DATABASE_LOCATION


@dataclass
class DatabaseManager:
    db_location: str

    def __post_init__(self):
        self.vocabulary_location = os.path.join(self.db_location, "vocabulary.csv")
        self.meta_location = os.path.join(self.db_location, "meta.csv")
        self.noun_location = os.path.join(self.db_location, "nouns.csv")
        self.verb_location = os.path.join(self.db_location, "verbs.csv")


DB_MANAGER = DatabaseManager(DATABASE_LOCATION)
