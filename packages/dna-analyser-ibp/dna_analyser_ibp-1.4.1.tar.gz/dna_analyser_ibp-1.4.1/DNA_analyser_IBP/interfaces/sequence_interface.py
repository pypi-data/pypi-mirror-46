# sequence_interface.py
# !/usr/bin/env python3
"""Library with Sequence interface object
Available classes:
Sequence - interface for interaction with sequence api
"""

import time
import pandas as pd

from typing import List, Union
from ..callers.user_caller import User

from ..statusbar import status_bar

from ..callers.sequence_caller import (
    NCBISequenceFactory,
    TextSequenceFactory,
    FileSequenceFactory,
    seq_delete,
    seq_load_all,
    seq_load_by_id,
    seq_load_data,
)


class Sequence:
    def __init__(self, user: User):
        self.user = user

    def load_all(self, filter_tag: List[str] = None) -> pd.DataFrame:
        """
        Return all or tag filtered sequence dataframe.
        :param filter_tag: tags for filtering result dataframe
        :return: pandas dataframe with sequences
        """
        seq = [se for se in seq_load_all(user=self.user, filter_tag=filter_tag)]
        data = pd.concat([s.get_dataframe() for s in seq], ignore_index=True)
        return data

    def load_by_id(self, id: str) -> pd.DataFrame:
        """
        Return sequence dataframe by given id.
        :param id: id for getting result dataframe
        :return: pandas dataframe with sequence
        """
        seq = seq_load_by_id(user=self.user, id=id)
        return seq.get_dataframe()

    def load_data(self, sequence: pd.Series, data_len: int = 100, pos: int = 0):
        """
        Return string with loaded data of selected sequence.
        :param sequence: sequence pandas Series
        :param data_len: length of data
        :param pos: start position
        :return: string with returned data
        """
        return seq_load_data(
            user=self.user, id=sequence["id"], data_len=data_len, pos=pos
        )

    def text_creator(
        self, circular: bool, data: str, name: str, tags: List[str], sequence_type: str
    ):
        """
        Send request with text data and refresh API object with added sequence.
        :param circular: if sequence is circular or not
        :param data: raw text data string with sequence
        :param name: name of sequence
        :param tags: list of sequence tags eg. ['test', 'test2']
        :param sequence_type: string DNA / RNA
        """

        # start Text sequence factory
        status_bar(
            user=self.user,
            func=lambda: TextSequenceFactory(
                user=self.user,
                circular=circular,
                data=data,
                name=name,
                tags=tags,
                sequence_type=sequence_type,
            ),
            name=name,
            cls_switch=True,
        )

    def ncbi_creator(self, circular: bool, name: str, tags: List[str], ncbi_id: str):
        """
        Send request with NCBI id and refresh API object with added NCBI sequence.
        :param circular: if sequence is circular or not
        :param name: name of sequence
        :param tags: list of sequence tags eg. ['test', 'test2']
        :param ncbi_id: id of sequence from [https://www.ncbi.nlm.nih.gov/]
        """

        # start NCBI sequence factory
        status_bar(
            user=self.user,
            func=lambda: NCBISequenceFactory(
                user=self.user, circular=circular, name=name, tags=tags, ncbi_id=ncbi_id
            ),
            name=name,
            cls_switch=True,
        )

    def file_creator(
        self,
        circular: bool,
        file_path: str,
        name: str,
        tags: List[str],
        sequence_type: str,
        format: str,
    ):
        """
        Creates sequence for current user from PLAIN or FASTA data file.
        :param user: user for auth
        :param circular: if sequence is circular or not
        :param file_path: path to your file
        :param name: name of sequence
        :param tags: list of sequence tags eg. ['test', 'test2']
        :param sequence_type: string DNA / RNA
        :param format FASTA or PLAIN
        """

        # start File sequence factory
        status_bar(
            user=self.user,
            func=lambda: FileSequenceFactory(
                user=self.user,
                circular=circular,
                file_path=file_path,
                name=name,
                tags=tags,
                sequence_type=sequence_type,
                format=format,
            ),
            name=name,
            cls_switch=True,
        )

    def delete(self, sequence_dataframe: Union[pd.DataFrame, pd.Series]):
        """
        Delete given sequence or sequences.
        :param sequence_dataframe: dataframe with multiple sequences or series with one
        """
        if isinstance(sequence_dataframe, pd.DataFrame):
            for _, row in sequence_dataframe.iterrows():
                _id = row["id"]
                if seq_delete(user=self.user, id=_id):
                    print(f"Sequence {_id} was deleted")
                    time.sleep(1)
                else:
                    print("Sequence cannot be deleted")
        else:
            _id = sequence_dataframe["id"]
            if seq_delete(user=self.user, id=_id):
                print(f"Sequence {_id} was deleted")
            else:
                print("Sequence cannot be deleted")
