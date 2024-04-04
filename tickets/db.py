# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import sqlalchemy as sa
from common.settings import settings

engine = sa.create_engine(settings.DSN)  # Fill in DSN
metadata = sa.MetaData()
