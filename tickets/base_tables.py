# -*- coding: utf-8 -*-
from __future__ import annotations

import pandas as pd
from .db import engine


class BaseOrdersCleaner(object):
    SCHEMA_NAME = 'transfers'

    FIELDS_MAP = {
        '序号': 'serial_number',
        '订单号 Order Number': 'order_number',
        '转票人姓名 Transferer\'s name': 'source_member_name',
        '转票人手机号 Transferer\'s phone number': 'source_member_phone',
        '转票人邮箱 Transferee\'s Email address': 'source_member_email',
        '受让人姓名 Transferee\'s name': 'destination_member_name',
        '受让人手机号 Transferee\'s phone number': 'destination_member_phone',
        '受让人邮箱 Transferee\'s Email address': 'destination_member_email',
        '受让人俱乐部 Transferee\'s club name': 'destination_club_name',
        '受让人城市 Transferee city': 'destination_city',
        '受让人所在中区 Transferee\'s Division': 'destination_division',
        '受让人所在小区 Transferee\'s Area': 'destination_area',
        '受让人微信号 Transferee\'s Wechat account': 'destination_wechat',
        '提交人': 'submitted_by',
        '修改人': 'modified_by',
        '提交时间': 'submitted_at',
        '修改时间': 'updated_at',
        '填写时长': 'filling_duration',
        '填写设备': 'device',
        '操作系统': 'operating_system',
        '浏览器': 'browser',
        '填写地区': 'location',
        'IP': 'ip_address',
    }

    def read_raw(self, input_file: str) -> pd.DataFrame:
        df = pd.read_excel(input_file, sheet_name='Sheet1', engine='openpyxl')
        df = df.rename(columns=self.FIELDS_MAP)

        return df

    def save(self, df: pd.DataFrame):
        df.to_sql(self.SCHEMA_NAME, engine, if_exists='replace', index=False)
