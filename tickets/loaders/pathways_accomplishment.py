# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import pandas as pd
from common.constants import COMMASPACE, SPACE, COMMA, FULL_WIDTH_COMMA, NAME_UNAVAILABLE, DASH
from .base import AbstractLoader
from ..db import get_member_name_by_id


class PathwaysAccomplishmentLoader(AbstractLoader):

    """
    Club	Division	Area	Award	Date	Member	Name

    """

    OUTPUT_SCHEMA = 'pathways_accomplishment'

    RECOGNITION_AWARD_TYPE = 'Pathways 通关奖'

    FIELDS_MAP = {
        'Club': 'club_id',
        'Division': 'division',
        'Area': 'area',
        'Award': 'pathways_credit',
        'Date': 'date',
        'Member': 'member_name',
        'Name': 'club_name'
    }

    FIELDS_REQUIRES_TYPE_CASTING = {
        'area': str
    }

    @staticmethod
    def clean_name_unavailable(name: str) -> (str, str, str):
        if NAME_UNAVAILABLE not in name:
            return name, None

        member_id, _ = name.split(DASH, 1)
        member_id = member_id.strip()

        name, name_vector = get_member_name_by_id(member_id)
        return member_id, name, name_vector

    def transform_member_name(self, df: pd.DataFrame) -> pd.DataFrame:

        def _extract(name: str):
            if not isinstance(name, str):
                return pd.Series(dict(member_id=None,
                                      member_name=name,
                                      education_title=None,
                                      name_vector=None))

            if NAME_UNAVAILABLE in name:
                member_id, name, name_vector = self.clean_name_unavailable(name)
                if name_vector:
                    return pd.Series(dict(member_id=member_id,
                                          member_name=name,
                                          education_title=None,
                                          name_vector=name_vector))

            name = name.replace(FULL_WIDTH_COMMA, COMMA)
            try:
                name, education_title = name.split(COMMASPACE, 1)
            except ValueError:
                education_title = None

            name_vector = name.lower().replace('-', '').split(SPACE)
            name_vector = sorted(name_vector)
            name_vector = COMMA.join(name_vector)

            return pd.Series(dict(member_id=None,
                                  member_name=name,
                                  education_title=education_title,
                                  name_vector=name_vector))

        df[['member_id', 'member_name', 'education_title', 'name_vector']] = df['member_name'].apply(_extract)

        return df

    def append_recognition_award(self, df: pd.DataFrame) -> pd.DataFrame:
        df['recognition_award'] = self.RECOGNITION_AWARD_TYPE
        return df

    def run(self, path: str, sheet_name: str = 'Sheet 1', **__):
        df = self.extract_raw(path, sheet_name)
        df = self.transform_cast_types(df)
        df = self.transform_member_name(df)
        df = self.append_recognition_award(df)
        df = self.load_db(df)
        return df
