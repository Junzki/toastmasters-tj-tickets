# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401
from .pathways_accomplishment import PathwaysAccomplishmentLoader


class PathwaysDTMLoader(PathwaysAccomplishmentLoader):

    OUTPUT_SCHEMA = 'pathways_dtm'

    RECOGNITION_AWARD_TYPE = 'DTM 奖'

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

    def run(self, path: str, sheet_name: str = 'Sheet 1', **__):
        df = self.extract_raw(path, sheet_name)
        df = self.transform_cast_types(df)
        df = self.transform_member_name(df)
        df = self.append_recognition_award(df)
        df = self.load_db(df)
        return df
