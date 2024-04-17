# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import pandas as pd
from tickets.db import engine


class AbstractLoader(object):

    OUTPUT_SCHEMA: str
    FIELDS_MAP: ty.Dict[str, str]
    FIELDS_REQUIRES_TYPE_CASTING: ty.Dict[str, type]

    def run(self, path: str, sheet_name: str = 'Sheet 1', **kwargs) -> pd.DataFrame:
        raise NotImplementedError()

    def transform_cast_types(self, df: pd.DataFrame) -> pd.DataFrame:
        for field, type_ in self.FIELDS_REQUIRES_TYPE_CASTING.items():
            df[field] = df[field].astype(type_)

        return df

    def extract_raw(self, path: str, sheet_name: str = 'Sheet 1', **__) -> pd.DataFrame:
        df = pd.read_excel(path, sheet_name=sheet_name)
        df = self.transform_field_names(df)

        return df

    def transform_field_names(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = list(self.FIELDS_MAP.values())
        df = df.rename(columns=self.FIELDS_MAP)
        return df[columns]

    def load_db(self, df: pd.DataFrame) -> pd.DataFrame:
        df.to_sql(self.OUTPUT_SCHEMA, engine, if_exists='replace', index=True, index_label='id')
        return df
