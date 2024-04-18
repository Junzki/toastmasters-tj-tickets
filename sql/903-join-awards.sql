select merged.division,
       merged.area,
       merged.club_id,
       merged.club_name,
       merged.member_id,
       merged.member_name,
       merged.awards,
       ra.email_address,
       ra.phone,
       ra.wechat,
       ra.purchased_ticket
from (select division,
                      area,
                      club_id,
                      club_name,
                      member_id,
                      member_name,
                      string_agg(award, '; ') as "awards",
                      min(id)                 as id
               from recognition_awards
               group by division,
                        area,
                        club_id,
                        club_name,
                        member_id,
                        member_name
               order by division, area, club_id) "merged"
left join recognition_awards ra on ra.id = merged.id
order by merged.division, merged.area, merged.club_id;
