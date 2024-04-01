# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import click
import pandas as pd

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
    '我已阅读说明了解规则': 'read_rules',
    '经确认我已获得认可奖': 'recognition_award',
    '姓名': 'name',
    '所获得的认可奖': 'awards',
    '会员号（8位数字）': 'member_id',
    '手机号': 'phone',
    '邮箱': 'email',
    '俱乐部全称': 'club_name',
    '所属中区': 'division',
    '所属小区': 'area',
    '城市': 'city',
    '微信号': 'wechat',
}


@click.group()
def cli():
    ...


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def read_raw(input_file: str):
    return _read_raw(input_file)


def _read_raw(input_file: str):
    df = pd.read_excel(input_file)
    df = df[list(FIELDS_MAP.keys())]
    df = df.rename(columns=FIELDS_MAP)
    df = extract_raw_buyer_info(df)

    return df


def extract_raw_buyer_info(df: pd.DataFrame) -> pd.DataFrame:
    fields = [f[0] for f in BUYER_INFO_FIELDS_MAP]

    df = df['raw_buyer_info'].apply(_buyer_info_to_series)
    # df = df.drop(columns=['raw_buyer_info'])

    return df



def _buyer_info_to_series(in_: str) -> pd.Series:
    s = pd.Series(_clean_raw_buyer_info(in_))
    return s


def _clean_raw_buyer_info(in_: str) -> ty.Dict[str, str]:
    out_ = dict()
    if not in_:
        return out_

    groups = in_.split(';')
    for group in groups:
        key, value = group.split(':')
        if key in BUYER_INFO_FIELDS_MAP:
            key = BUYER_INFO_FIELDS_MAP[key]

        out_[key] = value

    out_['recognition_award'] = out_.get('recognition_award') == '是'

    return out_


if __name__ == "__main__":
    cli()
