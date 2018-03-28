drop table if exists photos;

create table photos (
    id serial not null,
    filename text not null,
    type text not null,
    title text,
    keywords text,
    description text,
    width integer,
    height integer,
    date_created timestamp(0) without time zone not null default now(),
    date_modified timestamp(0) without time zone not null default now(),
    primary key (id),
    unique (filename)
);
   
