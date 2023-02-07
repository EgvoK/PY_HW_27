drop table if exists items;

create table items(
    id integer primary key autoincrement,
    created timestamp not null default current_timestamp,
    title text not null,
    description text not null
);