personal_pronouns = {
    "Nominative": {
        "1st-singular": "ich",
        "2nd-singular": "du",
        "3rd-singular-masculine": "er",
        "3rd-singular-feminine": "sie",
        "3rd-singular-neuter": "es",
        "1st-plural": "wir",
        "2nd-plural": "ihr",
        "3rd-plural": "sie",
        "2nd-formal": "Sie",
    },
    "Accusative": {
        "1st-singular": "mich",
        "2nd-singular": "dich",
        "3rd-singular-masculine": "ihn",
        "3rd-singular-feminine": "sie",
        "3rd-singular-neuter": "es",
        "1st-plural": "uns",
        "2nd-plural": "euch",
        "3rd-plural": "sie",
        "2nd-formal": "Sie",
    },
    "Dative": {
        "1st-singular": "mir",
        "2nd-singular": "dir",
        "3rd-singular-masculine": "ihm",
        "3rd-singular-feminine": "ihr",
        "3rd-singular-neuter": "ihm",
        "1st-plural": "uns",
        "2nd-plural": "euch",
        "3rd-plural": "ihnen",
        "2nd-formal": "Ihnen",
    },
    "Genitive": {
        "1st-singular": "meiner",
        "2nd-singular": "deiner",
        "3rd-singular-masculine": "seiner",
        "3rd-singular-feminine": "ihrer",
        "3rd-singular-neuter": "seiner",
        "1st-plural": "unser",
        "2nd-plural": "euer",
        "3rd-plural": "ihrer",
        "2nd-formal": "Ihrer",
    },
}

definitive_articles = {
    "Nominative": {
        "Masculine": "der",
        "Feminine": "die",
        "Neuter": "das",
        "Plural": "die",
    },
    "Accusative": {
        "Masculine": "den",
        "Feminine": "die",
        "Neuter": "das",
        "Plural": "die",
    },
    "Dative": {"Masculine": "dem", "Feminine": "der", "Neuter": "dem", "Plural": "den"},
    "Genitive": {
        "Masculine": "des",
        "Feminine": "der",
        "Neuter": "des",
        "Plural": "der",
    },
}

indefinite_articles = {
    "Nominative": {
        "Masculine": "ein",
        "Feminine": "eine",
        "Neuter": "ein",
        "Plural": "eine",
    },
    "Accusative": {
        "Masculine": "einen",
        "Feminine": "eine",
        "Neuter": "ein",
        "Plural": "eine",
    },
    "Dative": {
        "Masculine": "einem",
        "Feminine": "einer",
        "Neuter": "einem",
        "Plural": "einen",
    },
    "Genitive": {
        "Masculine": "eines",
        "Feminine": "einer",
        "Neuter": "eines",
        "Plural": "einer",
    },
}


# since just indefinite with `m`, just iterate over the indefinite articles
possessive_article = dict(indefinite_articles)
for k, v in possessive_article.items():
    for kk in v:
        possessive_article[k][kk] = f"m{possessive_article[k][kk]}"
