# -*- coding: utf-8
from __future__ import annotations

import typing as ty  # noqa: F401

import pandas as pd


class OrdersImporter(object):
    FIELDS_MAP = {
        '序号': ('id', int),
        '姓名': ('member_name', str),
        '所属俱乐部': ('club_name_raw', str),
        '俱乐部': ('club_name_simple', str),
        'Club Name Standard': ('club_name', str),
        '中区': ('division', str),
        '小区': ('area', str),
        '城市': ('city', str),
        '手机号': ('phone', str),
        '邮箱': ('email', str),
        '微信号': ('wechat', str),
        '认可票': ('recognition_award', str),
        '会员号/认可票填写': ('recognition_award_member_id', str),
        '订单号': ('order_id', str)
    }
