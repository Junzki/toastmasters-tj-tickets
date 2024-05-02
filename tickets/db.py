# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import sqlalchemy as sa
from sqlalchemy.sql import text
from pypika import Query, Table, Parameter, Order
from common.settings import settings

engine = sa.create_engine(settings.DSN)  # Fill in DSN
metadata = sa.MetaData()

Members = Table('members')


def get_member_name_by_id(member_id: str) -> (str, str):
    stmt = Query.from_(Members) \
                .select(Members.last_name,
                        Members.first_name,
                        Members.middle_name,
                        Members.name_vector) \
                .where(Members.member_id == Parameter(':member_id')) \
                .orderby(Members.membership_end, order=Order.desc) \
                .limit(1)

    with engine.connect() as conn:
        result = conn.execute(text(stmt.get_sql()), parameters=dict(
            member_id=member_id
        ))
        found = result.fetchone()
        if not found:
            return None, None

        last, first, middle, name_vector = found

    name = f'{last} {first} {middle}' if middle else f'{last} {first}'
    return name, name_vector
