# g4killer_interface.py
# !/usr/bin/env python3
"""Library with G4killer interface object
Available classes:
G4Killer - interface for interaction with g4killer api
"""
import pandas as pd

from ..callers.g4killer_caller import G4KillerAnalyseFactory
from ..callers.user_caller import User
from .tool_interface import ToolInterface


class G4Killer(ToolInterface):
    """Api interface for g4killer analyse caller"""

    def __init__(self, user: User):
        self.user = user

    def analyse_creator(self, origin_sequence: str, threshold: float) -> pd.DataFrame:
        """
        Send request with sequence string and create g4killer analyse.
        :param origin_sequence: original sequence string [text]
        :param threshold: required gscore value
        :return: g4killer results
        """
        gkill = G4KillerAnalyseFactory(
            user=self.user, origin_sequence=origin_sequence, threshold=threshold
        ).analyse

        return gkill.get_dataframe().T
