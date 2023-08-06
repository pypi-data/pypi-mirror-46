# g4hunter_interface.py
# !/usr/bin/env python3
"""Library with G4hunter interface object
Available classes:
G4Hunter - interface for interaction with g4hunter api
"""

import time
import os
import matplotlib.pyplot as plt
import pandas as pd

from .analyse_interface import AnalyseInterface
from ..statusbar import status_bar

from typing import List, Union
from ..callers.user_caller import User

from ..callers.g4hunter_caller import (
    G4HunterAnalyseFactory,
    g4_delete_analyse,
    g4_export_csv,
    g4_load_all,
    g4_load_by_id,
    g4_load_result,
    g4_load_heatmap,
)


class G4Hunter(AnalyseInterface):
    """Api interface for g4hunter analyse caller"""

    def __init__(self, user: User):
        self.user = user

    def load_all(self, filter_tag: List[str] = None) -> pd.DataFrame:
        """
        Return all or tag filtered g4hunter analyse dataframe.
        :param filter_tag: tags for filtering result dataframe
        :return: pandas dataframe with g4hunter analyses
        """
        g4 = [g4 for g4 in g4_load_all(user=self.user, filter_tag=filter_tag)]
        data = pd.concat([g.get_dataframe() for g in g4], ignore_index=True)
        return data

    def load_by_id(self, id: str) -> pd.DataFrame:
        """
        Return g4hunter dataframe by given id.
        :param id: id for getting result dataframe
        :return: pandas dataframe with g4hunter analyse
        """
        g4 = g4_load_by_id(user=self.user, id=id)
        return g4.get_dataframe()

    def load_results(self, g4hunter_analyse: pd.Series):
        """
        Return pandas dataframe with results of g4hunter analyse.
        :param g4hunter_analyse: pandas series with one g4hunter analyse
        :return: dataframe with results
        """
        return g4_load_result(user=self.user, id=g4hunter_analyse["id"])

    def load_heatmap(
        self,
        g4hunter_analyse: pd.Series,
        segment_count: int = 31,
        coverage: bool = False,
    ):
        """
        Return seaborn graph with heatmap.
        :param g4hunter_analyse: pandas series with one g4hunter analyse
        :param segment_count: number of segments in sequence
        :param coverage: if True show coverage heatmap if False show count heatmap
        """
        data = g4_load_heatmap(
            user=self.user, id=g4hunter_analyse["id"], segment_count=segment_count
        )

        ax = data[["coverage" if coverage else "count"]].plot(
            kind="bar", figsize=(14, 8), legend=True, fontsize=12
        )
        ax.set_xlabel("segments", fontsize=12)
        ax.set_ylabel("coverage [%/100]" if coverage else "count [-]", fontsize=12)
        plt.grid(color="k", linestyle="-", linewidth=0.1)
        plt.show()

    def analyse_creator(
        self,
        sequence: Union[pd.DataFrame, pd.Series],
        tags: List[str],
        threshold: float,
        window_size: int,
    ):
        """
        Send request with sequence and create g4hunter analyse.
        :param sequence: sequence to analyse
        :param tags: list of tags for created analyse
        :param threshold: threshold for g4hunter analyse
        :param window_size: window size for this analyse
        """
        # start g4hunter analyse factory

        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                status_bar(
                    user=self.user,
                    func=lambda: G4HunterAnalyseFactory(
                        user=self.user,
                        id=row["id"],
                        tags=tags,
                        threshold=threshold,
                        window_size=window_size,
                    ),
                    name=row["name"],
                    cls_switch=False,
                )
        else:
            status_bar(
                user=self.user,
                func=lambda: G4HunterAnalyseFactory(
                    user=self.user,
                    id=sequence["id"],
                    tags=tags,
                    threshold=threshold,
                    window_size=window_size,
                ),
                name=sequence["name"],
                cls_switch=False,
            )

    def export_csv(
        self, g4hunter_pandas: Union[pd.DataFrame, pd.Series], out_path: str, aggregate: bool = True
    ):
        """
        Export g4hunter analyse into csv file.
        :param g4hunter_pandas: pandas series with one g4hunter analyse
        :param out_path: output folder complete path
        :return: string with data in csv format
        """
        if isinstance(g4hunter_pandas, pd.Series):
            _id = g4hunter_pandas["id"]
            name = g4hunter_pandas["title"]
            file_path = os.path.join(out_path, f"{name}_{_id}.csv")

            with open(file_path, "w") as new_file:
                data = g4_export_csv(user=self.user, id=_id, aggregate=aggregate)
                new_file.write(data)
            print(f"file created -> {file_path}")
        # export multiple analyses
        else:
            for _, row in g4hunter_pandas.iterrows():
                _id = row["id"]
                name = row["title"]
                file_path = os.path.join(out_path, f"{name}_{_id}.csv")

                with open(file_path, "w") as new_file:
                    data = g4_export_csv(user=self.user, id=_id, aggregate=aggregate)
                    new_file.write(data)
                print(f"file created -> {file_path}")

    def delete(self, g4hunter_pandas: Union[pd.DataFrame, pd.Series]):
        """
        Delete given g4hunter analyse or g4hunter analyses.
        :param g4hunter_pandas: dataframe with multiple g4hunter analyses or series with one
        """
        if isinstance(g4hunter_pandas, pd.DataFrame):
            for _, row in g4hunter_pandas.iterrows():
                _id = row["id"]
                if g4_delete_analyse(user=self.user, id=_id):
                    print(f"G4hunter {_id} was deleted")
                    time.sleep(1)
                else:
                    print("G4hunter cannot be deleted")
        else:
            _id = g4hunter_pandas["id"]
            if g4_delete_analyse(user=self.user, id=_id):
                print(f"G4hunter {_id} was deleted")
            else:
                print(f"G4hunter cannot be deleted")
