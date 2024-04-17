# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import pandas as pd
from common.constants import COMMA


class MemberNameMixin(object):

    @staticmethod
    def build_member_name_vector(df: pd.DataFrame) -> pd.DataFrame:

        def _join(x):
            names = [x['last_name'], x['middle_name'], x['first_name']]
            names_clean = list()

            for n in names:
                if not n:
                    continue

                if not isinstance(n, str) and pd.isna(n):
                    continue

                n = str(n)  # Force string

                n = n.lower().strip()
                names_clean.append(n)

            names_clean = sorted(names_clean)
            return COMMA.join(names_clean)

        df['name_vector'] = df.apply(_join, axis=1)
        return df
