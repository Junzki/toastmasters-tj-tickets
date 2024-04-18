create table clubs
(
    id        serial
        primary key,
    club_id   bigint,
    club_name text not null,
    division  varchar(2) default NULL::character varying,
    area      varchar(2) default NULL::character varying
);


insert into clubs (club_name)
select distinct club_name
from members;

update clubs
set division = origin.division,
    area     = origin.area,
    club_id  = origin.club_id
from (select distinct members.division,
                      members.area,
                      members.club_id,
                      members.club_name
      from members) "origin"
where clubs.club_name = origin.club_name;
