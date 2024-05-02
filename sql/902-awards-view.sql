create table recognition_awards
(
    id               serial
        primary key,
    division         varchar(2),
    area             varchar(2),
    club_id          bigint,
    club_name        text,
    member_id        bigint,
    member_name      text,
    email_address    text,
    phone            text,
    award            text,
    wechat           text,
    purchased_ticket boolean default false not null,
    name_vector      text
);


insert into recognition_awards (division,
                                area,
                                club_id,
                                club_name,
                                member_id,
                                member_name,
                                email_address,
                                phone,
                                award,
                                name_vector,
                                wechat,
                                purchased_ticket)
    (select distinct (coalesce(c.division, m.division, awards.division)) division,
                     (coalesce(c.area, m.area, awards.area))             area,
                     (coalesce(c.club_id, m.club_id))                    club_id,
                     awards.club_name,
                     m.member_id,
                     awards.member_name,
                     m.email_address,
                     m.phone,
                     awards.recognition_award,
                     awards.name_vector,
                     o.wechat,
                     (select o.id is not null)                           purchased_ticket
     from (select p.division,
                  p.area,
                  p.club_id,
                  p.club_name,
                  p.member_name,
                  p.recognition_award,
                  p.name_vector
           from pathways_accomplishment p
           union all
           (select dtm.division,
                   dtm.area,
                   dtm.club_id,
                   dtm.club_name,
                   dtm.member_name,
                   dtm.recognition_award,
                   dtm.name_vector
            from pathways_dtm dtm)
           union all
           (select (select null)         division,
                   (select null)::text   area,
                   (select null)::bigint club_id,
                   mentors.club_name,
                   mentors.member_name,
                   mentors.recognition_award,
                   mentors.name_vector
            from pathways_mentors mentors)
           union all
           (select p.division, p.area, p.club_id, p.club_name, p.member_name, p.recognition_award, p.name_vector
            from pathways_progress p)
           union all
           (select ltm.division,
                   ltm.area,
                   (select null)::bigint club_id,
                   ltm.club_name,
                   ltm.member_name,
                   ltm.recognition_award,
                   ltm.name_vector
            from long_term_members ltm)) "awards"
              left join clubs c on awards.club_name = c.club_name
              left join members m on m.name_vector = awards.name_vector
              left join orders_old o on o.email = m.email_address or m.phone like '%' || o.phone || '%'
     order by division, area, club_id);
