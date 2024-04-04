# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import pandas as pd
from .db import engine


class RawOrderCleaner(object):
    FIELDS_MAP = {
        '订单编号': 'order_id',
        '订单状态': 'order_state',
        '下单时间': 'submitted_at',
        '支付时间': 'paid_at',
        '发货时间': 'delivered_at',
        '确认收货时间': 'confirmed_at',
        '支付方式': 'payment_method',
        '订单描述': 'raw_description',
        '商品名称': 'product_name',
        '发货状态': 'delivery_state',
        '商品件数': 'product_count',
        '商品ID': 'product_id',
        '实付金额': 'paid_amount',
        '收货人/提货人姓名': 'receiver_name',
        '收货人/提货人手机号': 'receiver_phone',
        '省': 'receiver_province',
        '市': 'receiver_city',
        '区': 'receiver_district',
        '收货/提货详细地址': 'receiver_address',
        '下单模板信息': 'raw_buyer_info',
        '买家留言': 'buyer_comment',
        '下单账号': 'order_account',
        '下单微信': 'order_wechat'
    }

    BUYER_INFO_FIELDS_MAP = {
        '经确认我已获得认可奖': 'recognition_award',
        '姓名': 'name',
        '所获得的认可奖': 'awards',
        '会员号（8位数字）': 'member_id',
        '手机号': 'phone',
        '邮箱': 'email',
        '俱乐部全称': 'club_name',
        '俱乐部': 'club_name',
        '所属中区': 'division',
        '所属小区': 'area',
        '城市': 'city',
        '微信号': 'wechat',
        '职位': 'position_in_district',
        '干事职位': 'role_in_club',
    }

    def get_output_columns(self):
        out_ = list(set(self.FIELDS_MAP.values())) + list(set(self.BUYER_INFO_FIELDS_MAP.values()))

        return out_

    def read_raw(self, input_file: str) -> pd.DataFrame:
        df = pd.read_excel(input_file)
        df = df[list(self.FIELDS_MAP.keys())]
        df = df.rename(columns=self.FIELDS_MAP)
        df['receiver_phone'] = df['receiver_phone'].astype(str)

        df = self.extract_raw_buyer_info(df)

        columns = self.get_output_columns()
        df = df[columns]

        return df

    def save(self, df: pd.DataFrame):
        df.to_sql('orders', engine, if_exists='replace', index=False)

    def output_proceed(self, out_path: str, df: pd.DataFrame):
        df.to_excel(out_path)

    def extract_raw_buyer_info(self, df: pd.DataFrame) -> pd.DataFrame:
        extracted = df['raw_buyer_info'].apply(self._buyer_info_to_series)
        extracted['phone'] = extracted['phone'].astype(str)

        extracted['member_id'] = extracted['member_id'].apply(self.cast_member_id_to_pn)

        df = df.join(extracted)
        return df

    def cast_member_id_to_pn(self, member_id: int | None) -> ty.Optional[str]:
        if not member_id:
            return None

        member_id = '%s' % member_id
        if 'nan' == member_id:
            return None

        if len(member_id) != 8:
            pfx = '0' * (8 - len(member_id))
            member_id = f'{pfx}{member_id}'

        return f'PN-{member_id}'

    def _buyer_info_to_series(self, in_: str) -> pd.Series:
        s = pd.Series(self._clean_raw_buyer_info(in_))
        return s

    def _clean_raw_buyer_info(self, in_: str) -> ty.Dict[str, str]:
        out_ = dict()
        if not in_:
            return out_

        groups = in_.split(';')
        for group in groups:
            key, value = group.split(':')
            if key in self.BUYER_INFO_FIELDS_MAP:
                key = self.BUYER_INFO_FIELDS_MAP[key]
            else:
                continue

            out_[key] = value

        out_['recognition_award'] = out_.get('recognition_award') == '是'

        return out_
