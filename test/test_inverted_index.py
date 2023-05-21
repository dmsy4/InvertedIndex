import pytest
import string
import pandas as pd
from src.inverted_index import InvertedIndex
from src.encoding_utils import (
    delta_decode,
    delta_encode_seq,
    gamma_decode,
    gamma_encode_seq,
    identity,
)
from src.tokenizer import tokenize_text

def test_inverted_index():
    assert InvertedIndex('test_data/test1.csv')
    assert InvertedIndex(['test_data/test1.csv'], 'gamma', False)
    with pytest.raises(TypeError):
        assert InvertedIndex(1, 'gamma', True)
    assert InvertedIndex(['test_data/test1.csv', 'test_data/test2.csv'], 'gamma', False)
    k = InvertedIndex('test_data/test3.csv', 'gamma', True)
    k.create_inverted_index()
    assert k.index
    k = InvertedIndex('test_data/test1.csv', 'gamma', True)
    k.create_inverted_index()
    res = k.search('СПБГУ', False)
    assert res 
    k = InvertedIndex('test_data/test1.csv', 'gamma', False)
    k.create_inverted_index()
    res = k.search('СПБГУ', False)
    assert res 
    k = InvertedIndex('test_data/test1.csv', 'gamma', False)
    k.create_inverted_index()
    res = k.search('asdbahsbdhh', False)
    assert len(res) == 0
    k = InvertedIndex('test_data/test1.csv', 'gamma', True)
    k.create_inverted_index()
    res = k.search('день дата', False)
    assert len(res) > -1
    k = InvertedIndex('test_data/test1.csv', 'gamma', True)
    k.create_inverted_index()
    res = k.search('СПБГУ ректор', True)
    assert len(res) == 2