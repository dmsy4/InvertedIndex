import pytest
import string
import pandas as pd
from src.encoding_utils import (
    delta_decode,
    delta_encode_seq,
    _delta_encode,
    gamma_decode,
    gamma_encode_seq,
    _gamma_encode,
    identity,
)
from random import randint, sample

def test_encoding_utils():
    for _ in range(10):
        A = randint(0, 100000)
        assert [A] == delta_decode(_delta_encode(A))
    for _ in range(10):
        A = randint(0, 100000)
        assert [A] == gamma_decode(_gamma_encode(A))
    A = [randint(0, 50000)]
    assert A == identity(identity(A))
    for _ in range(10):
        A = [randint(0, 100000)]
        assert A == delta_decode(delta_encode_seq(A))
    for _ in range(10):
        A = [randint(0, 100000)]
        assert A == gamma_decode(gamma_encode_seq(A))
    A = 0
    with pytest.raises(ValueError):
        assert _gamma_encode(A)
    A = 1
    assert _gamma_encode(1)
    A = sample(range(1, 50000), 10)
    assert A == gamma_decode(gamma_encode_seq(A))

test_encoding_utils()