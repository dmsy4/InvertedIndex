import pandas as pd
from typing import List, Union
from tqdm.notebook import tqdm
import sys
from encoding_utils import (
    gamma_encode_seq,
    delta_encode_seq,
    gamma_decode,
    delta_decode,
    identity,
)
from tokenizer import tokenize_text


class InvertedIndex:
    def __init__(
        self,
        csv_paths: Union[List[str], str],
        encoding: Union[None, str] = None,
        encode_differences: bool = True,
    ) -> None:
        if isinstance(csv_paths, str):
            self._csv_paths = [csv_paths]
        elif isinstance(csv_paths, list):
            self._csv_paths = csv_paths
        else:
            raise TypeError("csv_paths must be either list or str")

        self.index = dict()

        assert encoding in [
            "gamma",
            "delta",
            None,
        ], "Only Gamma, Delta encoding is supported. Or none of this."
        self._encoding = encoding
        _encoding_funcs = {
            "gamma": gamma_encode_seq,
            "delta": delta_encode_seq,
            None: identity,
        }
        self._encode = _encoding_funcs[encoding]
        _decoding_funcs = {
            "gamma": gamma_decode,
            "delta": delta_decode,
            None: identity,
        }
        self._decode = _decoding_funcs[encoding]

        self._encode_differences = encode_differences

        print("Processing passed csv_paths")
        self._data_frames = None
        for csv_path in self._csv_paths:
            if self._data_frames is None:
                self._data_frames = pd.read_csv(csv_path, index_col="Unnamed: 0")
                if "Unnamed: 0" in self._data_frames:
                    self._data_frames = self._data_frames.set_index(
                        "Unnamed: 0"
                    ).reset_index(drop=True)
            else:
                df = pd.read_csv(csv_path, index_col="Unnamed: 0")
                if "Unnamed: 0" in df:
                    df = self._data_frames.set_index("Unnamed: 0").reset_index(
                        drop=True
                    )
                self._data_frames = pd.concat([self._data_frames, df])
        self._data_frames["post_id"] = range(1, len(self._data_frames) + 1)

        # no limit for str <-> int conversion (default limit is 4200)
        sys.set_int_max_str_digits(0)

    def create_inverted_index(self):
        doc_ids = self._data_frames.post_id
        texts = self._data_frames.text
        for doc_id, text in tqdm(zip(doc_ids, texts), total=len(self._data_frames)):
            # if doc_id == 50:
            #     break
            doc_tokens = tokenize_text(text)
            last = 0
            for token in set(doc_tokens):
                if token not in self.index:
                    self.index[token] = []
                # if self._encode_differences:
                #     delta_diff = doc_id - last
                #     self.index[token].append(delta_diff)
                #     last = doc_id
                # else:
                self.index[token].append(doc_id)

        if self._encode_differences:
            for token in self.index:
                last = 0
                for i, doc_id in enumerate(self.index[token]):
                    current = doc_id
                    self.index[token][i] = current - last
                    last = current

        for token in self.index:
            doc_ids_for_token = self.index[token]
            encoded_doc_ids = self._encode(doc_ids_for_token)
            self.index[token] = encoded_doc_ids

    def search(self, query: str, output_docs: bool = False):
        query_tokens = tokenize_text(query)
        relevant_doc_ids_for_query = None
        for query_token in query_tokens:
            if query_token not in self.index:
                continue
            encoded_post_lists = self.index[query_token]  # posting_lists
            decoded_post_lists = self._decode(encoded_post_lists)
            relevant_doc_ids_for_token = [decoded_post_lists[0]]
            for doc_id in decoded_post_lists[1:]:
                if self._encode_differences:
                    relevant_doc_ids_for_token.append(
                        relevant_doc_ids_for_token[-1] + doc_id
                    )
                else:
                    relevant_doc_ids_for_token.append(doc_id)

            if relevant_doc_ids_for_query is None:
                relevant_doc_ids_for_query = set(relevant_doc_ids_for_token)
            else:
                relevant_doc_ids_for_query &= set(relevant_doc_ids_for_token)
        relevant_doc_ids_for_query = (
            relevant_doc_ids_for_query
            if relevant_doc_ids_for_query is not None
            else set()
        )
        if output_docs:
            docs = self._data_frames[
                self._data_frames.post_id.isin(relevant_doc_ids_for_query)
            ].text.values
            return relevant_doc_ids_for_query, docs
        return relevant_doc_ids_for_query
