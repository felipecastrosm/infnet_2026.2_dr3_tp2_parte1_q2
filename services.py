import re
from functools import lru_cache

from transformers import Pipeline, pipeline

MODEL_NAME = "Helsinki-NLP/opus-mt-en-fr"
BATCH_SIZE = 8
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")


@lru_cache
def get_translator() -> Pipeline:
    return pipeline("translation_en_to_fr", model=MODEL_NAME)


def split_into_sentences(paragraph: str) -> list[str]:
    return [sentence for sentence in SENTENCE_BOUNDARY.split(paragraph.strip()) if sentence]


def translate(text: str) -> str:
    paragraphs = [split_into_sentences(line) for line in text.splitlines() if line.strip()]
    sentences = [sentence for paragraph in paragraphs for sentence in paragraph]
    results = iter(get_translator()(sentences, truncation=True, batch_size=BATCH_SIZE))
    return "\n".join(
        " ".join(next(results)["translation_text"] for _ in paragraph) for paragraph in paragraphs
    )
