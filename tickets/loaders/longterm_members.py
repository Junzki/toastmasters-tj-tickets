# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401
from .pathways_accomplishment import PathwaysAccomplishmentLoader


class LongTermMembersLoader(PathwaysAccomplishmentLoader):

    OUTPUT_SCHEMA = 'long_term_members'

    RECOGNITION_AWARD_TYPE = '资深会员奖'

    FIELDS_MAP = {
        'Club Name': 'club_name',
        'Division': 'division',
        'Area': 'area',
        'Original Join Date': 'original_join_date',
        'Member Name': 'member_name',
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
