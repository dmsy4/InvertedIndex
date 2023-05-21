import pytest
from src.tokenizer import tokenize_text

def test_tokenizer():
    string = 'вуз'
    assert tokenize_text(string) == [string]
    string = '«СПБГУ»'
    assert tokenize_text(string) == ['спбгу']

