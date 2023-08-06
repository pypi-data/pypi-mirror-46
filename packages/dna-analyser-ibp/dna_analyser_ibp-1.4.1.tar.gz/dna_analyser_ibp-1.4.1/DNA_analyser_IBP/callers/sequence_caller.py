# sequence_caller.py
# !/usr/bin/env python3
"""Library with Sequence object.
Available classes:
- Sequence: Sequence object
- TextSequenceFactory: sequence factory from raw text
- NCBISequenceFactory: sequence factory from NCBI database
- FileSequenceFactory: sequence factory from local file

"""

import abc
import json
from typing import Generator, List, Union

import pandas as pd
from requests_toolbelt import MultipartEncoder
import requests

from .user_caller import User
from ..utils import validate_key_response, validate_text_response


class SequenceModel:
    """Sequence class."""

    def __init__(self, **kwargs):
        self.id = kwargs.pop("id")
        self.name = kwargs.pop("name")
        self.created = kwargs.pop("created")
        self.type = kwargs.pop("type")
        self.circular = kwargs.pop("circular")
        self.length = kwargs.pop("length")
        self.ncbi = kwargs.pop("ncbi")
        self.tags = ", ".join(kwargs.pop("tags"))
        self.fasta_comment = kwargs.pop("fastaComment")
        self.nucleic_count = str(kwargs.pop("nucleicCounts"))

    def __str__(self):
        return f"id: {self.id} name: {self.name} type: {self.type}"

    def __repr__(self):
        return f"<Sequence {self.id} {self.name} {self.type}>"

    def get_dataframe(self) -> pd.DataFrame:
        """
        Returns pandas dataframe for current object.
        :return: pandas dataframe
        """
        data = pd.DataFrame().from_records(
            self.__dict__, columns=self.__dict__.keys(), index=[0]
        )
        return data


class SequenceFactory(metaclass=abc.ABCMeta):
    """Abstract class for others sequence factories."""

    def __init__(self, **kwargs):
        self.sequence = self.create_sequence(**kwargs)

    @abc.abstractmethod
    def create_sequence(self, **kwargs) -> Union[SequenceModel, Exception]:
        """Creates sequence with different calls on Api."""
        raise NotImplementedError("You should implement this!")


class TextSequenceFactory(SequenceFactory):
    """Sequence factory used for generating sequence from raw text or text file."""

    def create_sequence(
        self,
        user: User,
        circular: bool,
        data: str,
        name: str,
        tags: List[str],
        sequence_type: str,
    ) -> Union[SequenceModel, Exception]:
        """
        Creates sequence for current user from raw data string.
        :param user: user for auth
        :param circular: if sequence is circular or not
        :param data: raw text data string with sequence
        :param name: name of sequence
        :param tags: list of sequence tags eg. ['test', 'test2']
        :param sequence_type: string DNA / RNA
        :return: Sequence object or raise exception
        """
        header = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": user.jwt,
        }
        data = json.dumps(
            {
                "circular": circular,
                "data": data,
                "format": "PLAIN",
                "name": name,
                "tags": tags,
                "type": sequence_type,
            }
        )

        response = requests.post(
            f"{user.server}/sequence/import/text", headers=header, data=data
        )
        data = validate_key_response(
            response=response, status_code=201, payload_key="payload"
        )
        return SequenceModel(**data)


class FileSequenceFactory(SequenceFactory):
    """Sequence factory used for generating sequence from file"""

    def create_sequence(
        self,
        user: User,
        circular: bool,
        file_path: str,
        name: str,
        tags: List[str],
        sequence_type: str,
        format: str,
    ) -> Union[SequenceModel, Exception]:
        """
        Creates sequence for current user from raw data file.
        :param user: user for auth
        :param circular: if sequence is circular or not
        :param file_path: path to your file
        :param name: name of sequence
        :param tags: list of sequence tags eg. ['test', 'test2']
        :param sequence_type: string DNA / RNA
        :param format FASTA or PLAIN
        :return: Sequence object or raise exception
        """
        data = json.dumps(
            {
                "circular": circular,
                "format": format,
                "name": name,
                "tags": tags,
                "type": sequence_type,
            }
        )
        multi_encoder = MultipartEncoder(
            fields={"json": data, "file": ("filename", open(file_path, "rb"))}
        )

        header = {
            "Content-type": multi_encoder.content_type,
            "Accept": "application/json",
            "Authorization": user.jwt,
        }

        response = requests.post(
            f"{user.server}/sequence/import/file", headers=header, data=multi_encoder
        )
        data = validate_key_response(
            response=response, status_code=201, payload_key="payload"
        )
        return SequenceModel(**data)


class NCBISequenceFactory(SequenceFactory):
    """Sequence factory used for generating sequence from NCBI database."""

    def create_sequence(
        self, user: User, circular: bool, name: str, tags: List[str], ncbi_id: str
    ) -> Union[SequenceModel, Exception]:
        """
            Creates sequence for current user from ncbi id [https://www.ncbi.nlm.nih.gov/]
            :param user: user for auth
            :param circular: if sequence is circular or not
            :param name: name of sequence
            :param tags: list of sequence tags eg. ['test', 'test2']
            :param ncbi_id: id of sequence from [https://www.ncbi.nlm.nih.gov/]
            :return: created pandas dataframe
        """
        ncbi = [
            {
                "circular": circular,
                "name": name,
                "ncbiId": ncbi_id,
                "tags": tags,
                "type": "DNA",
            }
        ]
        data = json.dumps(
            {"circular": circular, "ncbis": ncbi, "tags": tags, "type": "DNA"}
        )
        header = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": user.jwt,
        }

        response = requests.post(
            f"{user.server}/sequence/import/ncbi", headers=header, data=data
        )
        data = validate_key_response(
            response=response, status_code=201, payload_key="items"
        )
        return SequenceModel(**data[0])


def seq_load_data(
    user: User, id: str, data_len: int, pos: int
) -> Union[str, Exception]:
    """
    Return string with data and sets data to object itself.
    :param user: user for auth
    :param id: sequence id
    :param data_len: len of loading data
    :param pos: starting position for data cut
    :return: data in string or tuple with error message
    """
    header = {
        "Content-type": "application/json",
        "Accept": "text/plain",
        "Authorization": user.jwt,
    }

    if pos >= 0 and 0 < data_len <= 1000:
        # params have to be in bounds
        params = {"len": data_len, "pos": pos}

        response = requests.get(
            f"{user.server}/sequence/{id}/data", headers=header, params=params
        )
        return validate_text_response(response=response, status_code=200)
    else:
        raise ValueError("Values out of range.")


def seq_delete(user: User, id: str) -> bool:
    """
    Delete sequence for given object.
    :param user: user for auth
    :param id: sequence id for deleting sequence
    :return: True if delete success and False if not
    """
    header = {
        "Content-type": "application/json",
        "Accept": "*/*",
        "Authorization": user.jwt,
    }

    response = requests.delete(f"{user.server}/sequence/{id}", headers=header)
    if response.status_code == 204:
        return True
    return False


def seq_load_all(
    user, filter_tag: List[str]
) -> Union[Generator[SequenceModel, None, None], Exception]:
    """
    Lists all available sequences for current user.
    :param user: user for auth
    :param filter_tag: user for auth
    :return: yields Sequence objects for load all sequences request
    """
    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }
    params = {
        "order": "ASC",
        "requestForAll": "true",
        "pageSize": "ALL",
        "tags": filter_tag if filter_tag else "",
    }

    response = requests.get(f"{user.server}/sequence", headers=header, params=params)
    data = validate_key_response(
        response=response, status_code=200, payload_key="items"
    )
    for record in data:
        yield SequenceModel(**record)


def seq_load_by_id(user: User, id: str) -> Union[SequenceModel, Exception]:
    """
    Lists one sequence for current user with current sequence id.
    :param user: logged in user
    :param id: sequence id
    :return: found sequence
    """
    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }

    response = requests.get(f"{user.server}/sequence/{id}", headers=header)
    data = validate_key_response(
        response=response, status_code=200, payload_key="payload"
    )
    return SequenceModel(**data)
