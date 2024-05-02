

from tickets.db import engine
import pandas as pd


def clean_awards():
    query = """
    select distinct on (b.member_id)
        r.division,
        r.area,
        r.club_id,
        r.club_name,
        b.member_id,
        r.member_name,
        r.member_email,
        r.member_phone,
        b.awards,
        o.order_id
    from (select member_id, string_agg(award, '、') awards
          from recognition_awards r
          where award not in ('俱乐部 Mentor', '俱乐部 Sponsor', '俱乐部 Coach')
          group by member_id) "b"
    inner join recognition_awards r on r.member_id = b.member_id
    left join orders o on r.member_email = o.email or r.member_phone like '%' || o.phone || '%'
    order by b.member_id;
    """

    df = pd.read_sql_query(query, engine)
    df['awards'] = df['awards'].apply(format_awards)
    return df


def format_awards(awards):
    awards = awards.split('、')

    result = ''
    limit = len(awards)

    for index, award in enumerate(awards):
        if not result:
            result += award
            continue

        ch = result[-1]
        if ch.isascii():
            result += ' '

        if index == limit - 1:
            result += '和'
            if award[0].isascii():
                result += ' '
        else:
            result += '、'

        result += award

    return result
