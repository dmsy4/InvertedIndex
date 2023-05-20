import nltk
from typing import List
import string
import pymorphy2


MORPH = pymorphy2.MorphAnalyzer()
nltk.download("stopwords")
STOP_WORDS = nltk.corpus.stopwords.words("russian")
STOP_WORDS.extend(nltk.corpus.stopwords.words("english"))
STOP_WORDS.extend(  # добавим некоторые пунктуационные знаки из текстов
    [
        "«",
        "»",
        ".)",
        '?.."',
        "..?",
        "--",
        "…",
        "...",
        "—",
        "–",
        ">.",
        ").",
        "&#",
        "])",
        "».",
        '".',
        "?..",
        "»,",
        '",',
        ",[",
        "['",
        "']",
    ]
)
WORD_TOKENIZER = nltk.WordPunctTokenizer()


def tokenize_text(text: str) -> List[str]:
    # text = text[2:-2]  # delete [''] symbols
    text_tokens = WORD_TOKENIZER.tokenize(text)
    text_tokens = [
        word
        for word in text_tokens
        if (
            word not in string.punctuation
            and word not in STOP_WORDS
            and not word.isnumeric()
        )
    ]
    text_tokens = [MORPH.parse(x)[0].normal_form for x in text_tokens]
    return text_tokens
