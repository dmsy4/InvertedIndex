from math import floor, log2
from typing import Any, Iterable, List


def _unary(x: int) -> str:
    return "1" * x + "0"


# ---- GAMMA ENCODING/DECODING ----
# https://en.wikipedia.org/wiki/Elias_gamma_coding
def _gamma_encode(x: int) -> int:
    N = floor(log2(x))
    unary_N = _unary(N)
    # hack to handle removing leading zeroes when converted to int
    # during decoding all 9's are replaced with 0
    if unary_N == "0":
        unary_N = "9"
    bin_x_without_MSB = bin(x)[
        3:
    ]  # for int(20): bin(20) = '10100', without Most significant bit -- '0100'
    return int(unary_N + bin_x_without_MSB)


def gamma_encode_seq(seq: Iterable[int]) -> int:
    encoded_seq = 0
    for s in seq:
        encoded_s = _gamma_encode(s)
        num_of_digits = len(str(encoded_s))
        encoded_seq = encoded_seq * (10**num_of_digits) + encoded_s
    return encoded_seq


def gamma_decode(encoded_seq: int) -> List[int]:  # x = 1110
    encoded_seq = str(encoded_seq).replace("9", "0")
    decoded_seq = []
    while len(encoded_seq) > 0:
        N = encoded_seq.find("0")  # for '11110' it is 4
        bin_decoded = "1" + encoded_seq[N + 1 : 2 * N + 1]  # add most significant bit
        encoded_seq = encoded_seq[2 * N + 1 :]
        # x = '1' + x[num_of_leading_ones + 1:]
        decoded_seq.append(int(bin_decoded, base=2))
    return decoded_seq


# ---- GAMMA ENCODING/DECODING ----


# ---- DELTA ENCODING/DECODING ----
# return zero if string is empty
def handle_empty_binary_string(x: str) -> str:
    return x if len(x) else "0"


def _delta_encode(x) -> int:
    gamma_encoded = str(_gamma_encode(1 + floor(log2(x))))
    binary_without_MSB = bin(x)[
        3:
    ]  # for int(20): bin(20) = '10100', without Most significant bit -- '0100'
    return int(gamma_encoded + binary_without_MSB)


def delta_encode_seq(seq: Iterable[int]) -> int:
    encoded_seq = 0
    for s in seq:
        encoded_s = _delta_encode(s)
        num_of_digits = len(str(encoded_s))
        encoded_seq = encoded_seq * (10**num_of_digits) + encoded_s
    return encoded_seq


# https://ru.wikipedia.org/wiki/%D0%94%D0%B5%D0%BB%D1%8C%D1%82%D0%B0-%D0%BA%D0%BE%D0%B4_%D0%AD%D0%BB%D0%B8%D0%B0%D1%81%D0%B0
def delta_decode(encoded_seq: int) -> List:
    encoded_seq = str(encoded_seq).replace("9", "0")
    decoded_seq = []
    while len(encoded_seq) > 0:
        M = encoded_seq.find("0")  # for '00001' it is 4
        first_part = encoded_seq[M + 1 : M + 1 + M]
        L = 2**M + int(handle_empty_binary_string(first_part), base=2)
        encoded_seq = encoded_seq[M + 1 + M :]
        second_part = encoded_seq[: L - 1]
        N = 2 ** (L - 1) + int(handle_empty_binary_string(second_part), base=2)
        encoded_seq = encoded_seq[L - 1 :]
        decoded_seq.append(N)
    return decoded_seq


# ---- DELTA ENCODING/DECODING ----


def identity(x: Any) -> Any:
    return x
