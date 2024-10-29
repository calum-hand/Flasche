from functools import wraps

import pandas as pd

from flasche.db.manager import DB_MANAGER


def validate_columns(required_columns):
    def decorator(func):
        @wraps(func)
        def wrapper(df: pd.DataFrame, *args, **kwargs):
            if required_columns != list(df.columns):
                raise ValueError(
                    f"Incorrect headers, expected: {required_columns} | got: {df.columns}"
                )
            return func(df, *args, **kwargs)

        return wrapper

    return decorator


def _insert(df: pd.DataFrame, location: str) -> None:
    """
    Insert data into the database.
    """
    df.to_csv(location, mode="a", header=False, index=False)


@validate_columns(["English", "German", "Type", "Level"])
def insert_general(df: pd.DataFrame) -> None:
    """
    Insert vocabulary into the database.
    """
    n_entries = len(df)
    meta = pd.DataFrame({"Correct": [0] * n_entries, "Incorrect": [0] * n_entries})
    _insert(df, DB_MANAGER.vocabulary_location)
    _insert(meta, DB_MANAGER.meta_location)


@validate_columns(["English", "Gender", "German", "Plural"])
def insert_nouns(df: pd.DataFrame) -> None:
    """
    Insert nouns into the database.
    """
    # Ensure nouns are capitalised
    df["English"] = df["English"].str.title()
    df["German"] = df["German"].str.title()
    _insert(df, DB_MANAGER.noun_location)


@validate_columns(["English", "Infinitive", "Tense", "Pronoun", "Conjugation"])
def insert_verbs(df: pd.DataFrame) -> None:
    """
    Insert verbs into the database.
    """
    _insert(df, DB_MANAGER.verb_location)
