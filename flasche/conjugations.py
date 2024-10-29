import io
from typing import List, Dict

import requests
from pypdf import PdfReader
import pandas as pd


def _build_url(value: str) -> str:
    return f"https://www.verbformen.com/conjugation/{value}.pdf"


def _sanitise_infinitive(infinitive: str) -> str:
    return (
        infinitive.replace("ä", "a3")
        .replace("ö", "o3")
        .replace("ü", "u3")
        .replace("ß", "s5")
    )


def download_conjugations(infinitive: str) -> List[io.BytesIO]:
    raw_conjugations = []
    infinitive = _sanitise_infinitive(infinitive)
    urls = [
        _build_url(f"{infinitive}{suffix}") for suffix in ["", "_hat", "_ist", "_unr"]
    ]

    for idx, url in enumerate(urls):
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            raw_conjugations.append(io.BytesIO(response.content))
            if idx == 0:
                break

    if not raw_conjugations:
        raise ValueError(f"No conjugations found for {infinitive}")

    return raw_conjugations


def extract_conjugations_from_pdf(pdf: io.BytesIO) -> List[List[str]]:
    reader = PdfReader(pdf)
    text = reader.pages[0].extract_text(extraction_mode="layout").split("\n")

    for idx, t in enumerate(text):
        if "Present" in t and "Imperfect" in t and "Perfect" in t:
            return [t.split() for t in text[idx + 1 : idx + 7] if t]

    raise ValueError("No conjugations found in PDF")


def parse_conjugations(conjugation_block: List[List[str]]) -> Dict[str, Dict[str, str]]:
    def _parse(v):
        return "".join([c for c in v if c.isalpha()])

    def _update(p):
        if p == "er":
            return "er/sie/es"
        elif p == "sie":
            return "sie/Sie"
        return p

    mapping = {
        "Present": {},
        "Imperfect": {},
        "Perfect": {},
    }

    for row in conjugation_block:
        mapping["Present"][_update(row[0])] = _parse(row[1])
        mapping["Imperfect"][_update(row[2])] = _parse(row[3])
        mapping["Perfect"][_update(row[-3])] = f"{row[-2]} {row[-1]}"

    return mapping


def collect_verb_conjugations(infinitive: str) -> List[Dict[str, Dict[str, str]]]:
    frames = []
    conjugations = download_conjugations(infinitive)

    for conj in conjugations:
        extracted = extract_conjugations_from_pdf(conj)
        extracted_2 = parse_conjugations(extracted)

        for k, v in extracted_2.items():
            d = pd.DataFrame(list(v.items()), columns=["Pronoun", "Conjugation"])
            d["Tense"] = k
            d["Infinitive"] = infinitive
            frames.append(d)

    df = (
        pd.concat(frames)[["Infinitive", "Tense", "Pronoun", "Conjugation"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    return df.drop_duplicates().reset_index(drop=True)
