# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import pandas as pd

from common.constants import COMMA
from .base import AbstractLoader
from .member_name_mixin import MemberNameMixin


class DistrictMemberLoader(AbstractLoader, MemberNameMixin):

    OUTPUT_SCHEMA = 'members'

    FIELDS_MAP = {
        'Region': 'region',
        'District': 'district',
        'Division': 'division',
        'Area': 'area',
        'Club ID': 'club_id',
        'Club Name': 'club_name',
        'Club Status': 'club_status',
        'Club Join Date': 'club_join_date',
        'Original Join Date': 'original_join_date',
        'Membership Begin': 'membership_begin',
        'Membership End': 'membership_end',
        'Member ID': 'member_id',
        'Paid Status': 'paid_status',
        'Last Name': 'last_name',
        'First Name': 'first_name',
        'Middle Name': 'middle_name',
        'EDU': 'edu',
        # 'Address Line 1': 'address_line_1',
        # 'Address Line 2': 'address_line_2',
        # 'City': 'city',
        # 'State': 'state',
        # 'Postal Code': 'postal_code',
        # 'Country': 'country',
        # 'Home Phone': 'home_phone',
        # 'Work Phone': 'work_phone',
        # 'Cell Phone': 'cell_phone',
        'Email Address': 'email_address',
        # 'Web URL': 'web_url',
        # 'Max Level Completed': 'max_level_completed',
        # 'Is Pathways Enrolled': 'is_pathways_enrolled'
    }

    FIELDS_REQUIRES_TYPE_CASTING = {
        'area': str,
        # 'home_phone': str,
        # 'work_phone': str,
        # 'cell_phone': str,
        # 'last_name': str,
        # 'middle_name': str,
        # 'first_name': str
    }

    def transform_cast_types(self, df: pd.DataFrame) -> pd.DataFrame:
        for field, type_ in self.FIELDS_REQUIRES_TYPE_CASTING.items():
            df[field] = df[field].astype(type_)

        return df

    def extract_raw(self, path: str, **__) -> pd.DataFrame:
        df = pd.read_excel(path)
        df = self.transform_field_names(df)
        df = self.transform_cast_types(df)
        return df

    def extract_is_pathways_enrolled(self, df: pd.DataFrame) -> pd.DataFrame:
        df['is_pathways_enrolled'] = df['is_pathways_enrolled'].apply(lambda x: x == 'Yes')
        return df

    def extract_phone(self, df: pd.DataFrame) -> pd.DataFrame:

        def _join(x):
            phones = x['home_phone'], x['work_phone'], x['cell_phone']
            phones_clean = list()

            for p in phones:
                if p in ('', None, 'nan', 'None'):
                    continue

                p = p.replace(' ', '').lstrip('86')
                phones_clean.append(p)

            phones_clean = list(set(phones_clean))

            return COMMA.join(phones_clean)

        df['phone'] = df.apply(_join, axis=1)
        return df

    def run(self, path: str, **__) -> pd.DataFrame:
        df = self.extract_raw(path)
        # df = self.extract_is_pathways_enrolled(df)
        # df = self.extract_phone(df)
        df = self.build_member_name_vector(df)

        df = self.load_db(df)
        return df
