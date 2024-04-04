# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import sqlalchemy as sa

engine = sa.create_engine('')  # Fill in DSN
metadata = sa.MetaData()
