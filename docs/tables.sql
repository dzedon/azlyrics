create table artist
(
    id         serial
        primary key,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null,
    name       varchar(50),
    url_name   varchar(50)
);

create table album
(
    id         serial
        primary key,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null,
    name       varchar(50),
    artist_id  integer
        references artist
);

create table song
(
    id         serial
        primary key,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null,
    name       varchar(50),
    album_id   integer
        references album
);

