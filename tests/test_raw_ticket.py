# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import unittest


class TestRawTicket(unittest.TestCase):
    def test_read_raw(self):
        import pandas as pd
        from tickets.raw_orders import _read_raw

        input_file = 'tests/fixtures/raw_tickets.xlsx'
        df = _read_raw(input_file)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (3, 21))

    def test_read_raw_buyer_info(self):
        from tickets.raw_orders import _clean_raw_buyer_info

        origin_ = '我已阅读说明了解规则:我已详细阅读并理解;经确认我已获得认可奖:是;姓名:Stephanie Xu Dan;' \
                  '所获得的认可奖:个人奖-晋级大区比赛的选手,个人奖-俱乐部资深会员奖/十年及以上马龄;' \
                  '会员号（8位数字）:940719;手机号:18640383490;邮箱:878929831@qq.com;' \
                  '俱乐部全称:Shenyang Mandarin TMC;所属中区:E;所属小区:4;城市:沈阳;微信号:xudanstephanie'

        expected = {
            'recognition_award': True,
            'name': 'Stephanie Xu Dan',
            'awards': '个人奖-晋级大区比赛的选手,个人奖-俱乐部资深会员奖/十年及以上马龄',
            'member_id': '940719',
            'phone': '18640383490',
            'email': '878929831@qq.com',
            'club_name': 'Shenyang Mandarin TMC',
            'division': 'E',
            'area': '4',
            'city': '沈阳',
            'wechat': 'xudanstephanie'
        }

        exact = _clean_raw_buyer_info(origin_)

        self.assertEqual(exact, expected)
