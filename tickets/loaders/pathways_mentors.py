# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401
from .pathways_accomplishment import PathwaysAccomplishmentLoader


class PathwaysMentorsLoader(PathwaysAccomplishmentLoader):

    OUTPUT_SCHEMA = 'pathways_mentors'

    RECOGNITION_AWARD_TYPE = 'Pathways 导师奖'

    FIELDS_MAP = {
        'Date': 'date',
        'Member': 'member_name',
        'Name': 'club_name'
    }

    def run(self, path: str, sheet_name: str = 'Sheet 1', **__):
        df = self.extract_raw(path, sheet_name)
        df = self.transform_member_name(df)
        df = self.append_recognition_award(df)
        df = self.load_db(df)
        return df
