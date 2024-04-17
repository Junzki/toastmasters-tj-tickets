# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

from .member_name_mixin import MemberNameMixin
from .pathways_accomplishment import PathwaysAccomplishmentLoader


class SmedleyAwardLoader(PathwaysAccomplishmentLoader,
                         MemberNameMixin):

    OUTPUT_SCHEMA = 'smedley_award'

    RECOGNITION_AWARD_TYPE = 'Smedley 奖'

    FIELDS_MAP = {
        '俱乐部编号': 'club_id',
        '中区': 'division',
        '小区': 'area',
        '教育等级': 'pathways_credit',
        '俱乐部名称': 'club_name',
        '干事职位': 'club_officer_title',
        '姓': 'last_name',
        '名': 'first_name',
        'Middle Name': 'middle_name',
    }

    FIELDS_REQUIRES_TYPE_CASTING = {
        'area': str,
    }

    def run(self, path: str, sheet_name: str = 'Sheet 1', **__):
        df = self.extract_raw(path, sheet_name)
        df = self.transform_cast_types(df)
        df = self.build_member_name_vector(df)
        df = self.append_recognition_award(df)
        df = self.load_db(df)
        return df
